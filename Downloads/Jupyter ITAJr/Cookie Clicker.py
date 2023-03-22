#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains

servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service = servico)
driver.get('https://orteil.dashnet.org/cookieclicker/')

sleep(5)
select_language = driver.find_element(By.ID, "langSelect-EN")
select_language.click()
sleep(5)
cookie = driver.find_element(By.ID, "bigCookie")
cookie_count = driver.find_element(By.ID, "cookies")
items = [driver.find_element(By.ID, "productPrice" + str(i)) for i in range(1, -1, -1)]

for i in range(1000):
    cookie.click()
    sleep(0.1)
    count = int(cookie_count.text.split(" ")[0])
    for item in items:
        price = int(item.text.replace(',', ''))
        if price <= count:
            actions = ActionChains(driver)
            actions.move_to_element(item)
            actions.click()
            actions.perform()

print('concluído')


# In[ ]:




