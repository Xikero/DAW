import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class SeleniumTestCase(unittest.TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()  
        self.driver.implicitly_wait(10)  

    def test_full_user_flow(self):
        driver = self.driver
        driver.get("http://127.0.0.1:5000/login")  

        # Iniciar sesión
        username_field = driver.find_element(By.NAME, "email")
        password_field = driver.find_element(By.NAME, "password")
        username_field.send_keys("selenium@selenium.com")
        password_field.send_keys("Selenium,2024@")
        password_field.send_keys(Keys.RETURN)
        time.sleep(2)  

        # Verificar que hemos sido redirigidos al perfil
        self.assertIn("profile", driver.current_url)
        self.assertIn("Bienvenid@", driver.page_source)

        # Navegar a la página de inicio
        driver.get("http://127.0.0.1:5000/index")
        self.assertIn("index", driver.current_url)

        # Navegar a la página de registro de incidencias
        driver.get("http://127.0.0.1:5000/register_incident")
        self.assertIn("register_incident", driver.current_url)

        # Completar el formulario de registro de incidencia
        project_field = driver.find_element(By.NAME, "project")
        description_field = driver.find_element(By.NAME, "description")
        position_field = driver.find_element(By.NAME, "position")
        responsible_field = driver.find_element(By.NAME, "responsible")
        status_field = driver.find_element(By.NAME, "status")

        project_field.send_keys("Madrid_T7")
        description_field.send_keys("Este es un incidente de prueba.")
        position_field.send_keys("Pintura")
        responsible_field.send_keys("Electrico")
        status_field.send_keys("Abierto")

        # Pulsar el botón de "Registrar Incidencia"
        register_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        register_button.click()
        time.sleep(2)  

        # Verificar que se redirige al dashboard
        self.assertIn("dashboard", driver.current_url)
        
        # Filtrar por proyecto específico
        project_filter = driver.find_element(By.NAME, "project")
        project_filter.send_keys("Madrid_T7")
        filter_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        filter_button.click()
        time.sleep(2)
        
        # Verificar que el proyecto se muestra en la tabla
        self.assertIn("Madrid_T7", driver.page_source)

        # Navegar a la página de KPIs
        driver.get("http://127.0.0.1:5000/kpis")
        self.assertIn("kpis", driver.current_url)
        self.assertIn("KPI", driver.page_source)

        # Realizar logout
        driver.get("http://127.0.0.1:5000/logout")
        self.assertIn("login", driver.current_url)

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
