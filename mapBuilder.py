
# Build a list of categories in the KrollCatalog
myItems = []
catHier = {}
catMap  = []
skuCatMap = []


def buildCategoryList(fileName):
    print("Starting....")
    file = open(fileName, 'r')
    lines = file.readlines()
    itemDict = {}
    itemStart = False
    for line in lines:
        # this is the start of a catalog item
        if line.__contains__("<KrollDealerCategoryExport>"):
            itemStart = True
        if itemStart:
            if line.__contains__("<CategoryId>"):
                categoryId = line
                categoryId = categoryId.replace("<CategoryId>", "")
                categoryId = categoryId.replace("</CategoryId>", "")
                itemDict['catId'] = categoryId
        if line.__contains__("<Name>"):
                categoryName = line
                categoryName = categoryName.replace("<Name>", "")
                categoryName = categoryName.replace("</Name>", "")
                itemDict['catName'] = categoryName
        if line.__contains__("<ParentID>"):
                categoryParentId = line
                categoryParentId = categoryParentId.replace("<ParentID>", "")
                categoryParentId = categoryParentId.replace("</ParentID>", "")
                itemDict['catParent'] = categoryParentId
        if line.__contains__("</KrollDealerCategoryExport>"):
                myItems.append(itemDict)
                itemDict = {}
                itemStart = False

    buildSkuCatMap()
    buildSkuCatNameMap()
    addCategorytoItems()

def buildSkuCatMap():
    inFile = open("KrollDealerCategoryProductExport.xml")
    outFile = open("skuTableTranslated.xml", 'w+')

    lines = inFile.readlines()

    for line in lines:
        if line.__contains__("<CategoryId>"):
            catId = line.replace("<CategoryId>","")
            catId = catId.replace("</CategoryId>","")
            catName = translateCatIdsToNames(catId)
            outFile.writelines("<CategoryId>"+catName+"</CategoryId>")
        else:
            outFile.write(line)


def addCategorytoItems():
    inFile = open("testDataSet.xml",'r')
    outFile = open("testDataSetCats.xml","w+")

    lines = inFile.readlines()
    skuStore = ""
    gotFromSku = False
    for line in lines:
        if line.__contains__("<SKU>"):
            skuStore = line.replace("<SKU>","")
            skuStore = skuStore.replace("</SKU>","")
            skuStore = skuStore.replace("  ","")
        if line.__contains__("<ParentSKU />"):
            itemCat = getCategoryForSku(skuStore)
            outFile.writelines(line)
            categoryLine = "<Category>"+itemCat.strip()+"</Category>\r\n"
            categoryLine.replace("  ","")
            outFile.writelines(categoryLine)
            gotFromSku = True
        if gotFromSku is False:
            if line.__contains__("<ParentSKU>"):
                itemSku = line.replace("<ParentSKU>", "")
                itemSku = itemSku.replace("</ParentSKU>", "")
                itemCat = getCategoryForSku(itemSku)
                categoryLine = "<Category>"+itemCat.strip()+"</Category>\r\n"
                categoryLine.replace("  ","")
                outFile.writelines(categoryLine)
        if line.__contains__("</KrollDealerCatalogProductExport>"):
            outFile.writelines(line)
            gotFromSku = False
        outFile.writelines(line)

def getCategoryForSku(sku):
    foundCatForSku = False
    logFile = open("logfile.txt",'w+')
    logFile.writelines("Got sku: " +sku)
    for item in skuCatMap:
        logFile.writelines("Checking sku: " +item['sku'])
        if item['sku'] == sku:
            foundCatForSku = True
            return item['catName']
    if foundCatForSku == False:
        return "Undefined"


def buildSkuCatNameMap():
    inFile = open("skuTableTranslated1.xml", 'r')

    lines = inFile.readlines()
    itemStart = False
    skuCatObject = {}
    for line in lines:
        if line.__contains__("<KrollDealerCategoryProductExport>"):
            itemStart = True
        if itemStart:
            if line.__contains__("<CategoryId>"):
                catName = line.replace("<CategoryId>","")
                catName = catName.replace("</CategoryId>", "")
                catName = catName.replace("  ","")
                skuCatObject['catName'] = catName
            if line.__contains__("<SKU>"):
                sku = line.replace("<SKU>","")
                sku = sku.replace("</SKU>","")
                sku = sku.replace("</CategoryId>", "")
                sku = sku.replace("  ","")
                skuCatObject['sku'] = sku
            if line.__contains__("</KrollDealerCategoryProductExport>"):
                skuCatMap.append(skuCatObject)
                skuCatObject = {}
                itemStart = False




def translateCatIdsToNames(targetId):
    catFound = False;
    for cat in myItems:
        if cat['catId'].__contains__(targetId):
            catFound = True
            return cat['catName'].replace("  ","")
    if catFound == False:
        return "Undefined"






buildCategoryList("KrollDealerCategoryExport.xml")