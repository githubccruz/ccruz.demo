
__author__ = 'Intellisys'

from PIL import Image
import photohash
from selenium import webdriver
import time

def imgCrop(image, box , name):
    region = image.crop(box)
    region.save(name+".png")

def get_box(positions):
    print (positions['x'] , positions['y'] ,positions['x'] + positions['width'], positions['y'] + positions['height'])
    return (positions['x'] , positions['y'] ,positions['x'] + positions['width'], positions['y'] + positions['height'])

def _save_image_if_not_exists(image_name):
    try:
        Image.open("old-"+image_name+".png")
    except:
        old_img =Image.open(image_name+".png")
        old_img.save("old-"+image_name+".png")



def compare_images(image_name):
    _save_image_if_not_exists(image_name)
    return photohash.is_look_alike(image_name+".png", "old-"+image_name+".png")

def save_element_image(driver, xpath ,output_name):
    element = driver.find_element_by_xpath(xpath)
    output = dict(element.size, **element.location)
    driver.save_screenshot(output_name+".png")
    screenshot = Image.open(output_name+".png")
    imgCrop(image=screenshot , box=get_box(output),name=output_name )

def check_image(driver,xpath,image_name):
    save_element_image(driver,xpath,image_name)
    return compare_images(image_name)

def remove_floating_ad(driver):
    driver.execute_script('a = document.getElementById("floatingAd");')
    driver.execute_script('a.parentNode.removeChild(a)')

driver = webdriver.Firefox()
driver.get("http://luckymag.com/")
remove_floating_ad(driver)
print check_image(driver,'//*[@id="site-header"]/div/div[2]/hgroup/h2/a', "cn_site_logo")
#driver.close()