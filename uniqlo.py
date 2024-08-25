from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def UniqloOffers():
    options = Options()
    options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    driver.get("https://www.uniqlo.com/sg/en/feature/sale/men?path=5856&flagCodes=discount")



    saleTitle = driver.find_elements(By.TAG_NAME, "h1") 
    for title in saleTitle: 
        print (title.text) 

    wholeContainer = driver.find_elements(By.CSS_SELECTOR, ".fr-contents-card.full") 
    salesDict = {}

    for i, container in enumerate(wholeContainer): 
        print (f"container {i} found")

        try:
            w12 = container.find_element(By.CSS_SELECTOR, ".w12.relative")
            # print (f" w12 found in the container {i}: {w12.text}") 
            print (f"w12 found in container {i}") 


            griditems = w12.find_elements(By.CSS_SELECTOR,".fr-grid-item.w4")
            for item in griditems:
                print(item.text)
                # item name and item price
                itemName = item.find_element(By.CSS_SELECTOR,".description.decscription-text.fr-no-uppercase").text
                itemPricewithCurrency = item.find_element(By.CSS_SELECTOR,".price-limited")

                # there are multiple spans element in itemPricewithCurrency, but the last one contains the actual price
                itemCurrency = itemPricewithCurrency.find_element(By.CSS_SELECTOR,".fr-no-uppercase").text
                itemPrice = itemPricewithCurrency.find_elements(By.TAG_NAME,"span")[-1].text
                print (itemName,itemCurrency,itemPrice)

                salesDict[itemName] = itemCurrency + itemPrice
                print ("----------------------------------------------------------------------")

            break

        except:
            print (f" w12 not found in the container {i}")


    #print (salesDict)
    driver.close()
    
    return salesDict


if __name__ == "__main__":
    UniqloOffers()