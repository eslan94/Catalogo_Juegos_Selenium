
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from acciones import AccionesCatalogo
import time

ruta_driver = "msedgedriver.exe"
service = Service(executable_path=ruta_driver)

driver = webdriver.Edge(service=service)
driver.maximize_window()

actions = AccionesCatalogo(driver)

try:    
    actions.login_portal("esteban_pro", "clave123")
    time.sleep(2)

    actions.add_game(
        titulo= "Elden Ring", 
        plataforma= "PS5", 
        estrellas= 5, 
        genero= "Action RPG", 
        url_portada= "https://i.redd.it/bueqtztxmnj81.png"
    )

    actions.delete_duplicate()

    actions.scroll_view()

    actions.goToStreamlit()

finally:
    
    time.sleep(10)
    driver.quit()