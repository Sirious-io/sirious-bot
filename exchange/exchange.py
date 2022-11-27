import json, os, secrets, eth_account, requests, config, exchange.web3Decode as web3Decode, sirious, discord

file = "exchange/keys.json"
pendingLinksFile = "exchange/pendingLinks.json"
WalletLinksFile = "exchange/WalletLinks.json"

#TODO: make this use firebase *partialy*

coin_ctx = sirious.sirious(config.config["CryptoNode"])

def writeFile(data, file = file):
    with open(file, 'w') as f:
        json.dump(data, f)

if not os.path.exists(file):
    privateKey = secrets.token_hex(32)
    publicKey = eth_account.Account.from_key("0x" + privateKey).address
    writeFile({"public": publicKey, "private": privateKey})
    privateKey, publicKey = None, None

if not os.path.exists(pendingLinksFile):
    writeFile({}, pendingLinksFile)

if not os.path.exists(WalletLinksFile):
    writeFile({}, WalletLinksFile)

def openFile(file = file):
    with open(file, 'r') as f:
        return json.load(f)



async def LinkedWalletsCheck(client):
    PendingLinks = openFile(file=pendingLinksFile)
    linked = []
    for id in PendingLinks.keys():
        txs = requests.get(config.config["CryptoNode"] + "/accounts/accountInfo/" + eth_account.Account.from_key("0x" + PendingLinks[id]["toPriv"]).address).json()["result"]["transactions"]
        if not txs == ["none"]:
            del txs["none"] # remove the 'none' tx
            toBeRefunded = 0
            validTX = False
            for txid in txs:
                tx = json.loads(requests.get(config.config["CryptoNode"] + "/get/transaction/" + txid).json()["result"]["data"])

                if tx["type"] == 0:
                    if tx["to"] == eth_account.Account.from_key("0x" + PendingLinks[id]["toPriv"]).address and tx["from"] == PendingLinks[id]["targetWallet"]:
                        toBeRefunded += tx["tokens"]
                        validTX = True
                
                elif tx["type"] == 2:
                    w3tx = web3Decode.DecodeRawTX(tx["rawTx"])
                    if w3tx["to"] == eth_account.Account.from_key("0x" + PendingLinks[id]["toPriv"]).address and w3tx["from"] == PendingLinks[id]["targetWallet"]:
                        toBeRefunded += w3tx["tokens"]
                        validTX = True
            
            if validTX: 
                links = openFile(file=WalletLinksFile)
                links = links[str(id)]=PendingLinks[id]["targetWallet"]
                writeFile(links, file=WalletLinksFile)

                sameWalletPendings = [k for k,v in dict((k.lower(), v) for k, v in PendingLinks.items()).items() if v == str(PendingLinks[id]["targetWallet"]).lower()]; sameWalletPendings.remove(str(PendingLinks[id]["targetWallet"]).lower())

                for id in sameWalletPendings:
                    del PendingLinks[id]
                    dm = await (client.get_user(int(id))).create_dm()
                    embed = discord.Embed()
                    embed.add_field(name="Unsuccessfully Linked wallet ``" + PendingLinks[id]["targetWallet"] + "``", value="Someone linked the wallet before you did! Committing fraud is uncool :(")
                    await dm.send(embed=embed)

            if toBeRefunded > 0:
                txid = coin_ctx.transaction(PendingLinks[id]["toPriv"], eth_account.Account.from_key("0x" + PendingLinks[id]["toPriv"]).address, PendingLinks[id]["targetWallet"], toBeRefunded)
                dm = await (client.get_user(int(id))).create_dm()
                embed = discord.Embed()
                embed.add_field(name="Successfully Linked wallet ``" + PendingLinks[id]["targetWallet"] + "``", value="Refund TXID: ``" + txid + "``")
                await dm.send(embed=embed)
                linked.append(id)

    if not linked == []:
        for id in linked:
            del PendingLinks[id]
        writeFile(PendingLinks, file=pendingLinksFile)


        


async def LinkWallet(ctx, walletAddr):
    if sirious.is_address(walletAddr):
        PendingLinks = openFile(file=pendingLinksFile)

        ValidPrivKey = False
        while not ValidPrivKey:
            privateKey = secrets.token_hex(32)
            ValidPrivKey = (requests.get(config.config["CryptoNode"] + "/accounts/accountInfo/" + eth_account.Account.from_key("0x" + privateKey).address).json()["result"]["transactions"]) == ["none"] and not privateKey in PendingLinks.values()
    
        PendingLinks[str(ctx.author.id)] = {"toPriv": privateKey, "targetWallet": walletAddr}
        writeFile(PendingLinks, file=pendingLinksFile)

        embed = discord.Embed()
        embed.add_field(name="Please send some " + config.config["CryptoName"] + " to ``" + eth_account.Account.from_key("0x" + privateKey).address, value="The full amount will be refunded.")
        await ctx.reply(embed=embed)
        privateKey = None
    else:
        embed = discord.Embed(title="❌  Error  ❌")
        embed.add_field(name="Inavlid wallet address!", value="Your address should start with ``0x``, please double check!")
        await ctx.reply(embed=embed)
    