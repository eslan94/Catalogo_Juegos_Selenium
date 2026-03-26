from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time

class AccionesCatalogo:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def login_portal(self, usuario, password):
        self.driver.get("http://localhost:80")
        print(f"Intentando login con: {usuario}")

        self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Usuario']"))).send_keys(usuario)
        self.driver.find_element(By.XPATH, "//input[@placeholder='Contraseña']").send_keys(password)

        self.driver.find_element(By.CLASS_NAME, "btn-primary").click()
        print("Login enviado.")

    def add_game(self, titulo, plataforma, estrellas, genero, url_portada):
        try:
            print(f"Añadiendo juego: {titulo}...")

            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1")))

            self.driver.find_element(By.XPATH, "//input[@placeholder='Título']").send_keys(titulo)
            self.driver.find_element(By.XPATH, "//input[@placeholder='Género']").send_keys(genero)
            self.driver.find_element(By.XPATH, "//input[@placeholder='URL de la Portada']").send_keys(url_portada)

            time.sleep(3)

            dropdown_plat = Select(self.driver.find_element(By.XPATH, "(//select)[1]"))
            dropdown_plat.select_by_value(plataforma)

            dropdown_rate_element = self.driver.find_element(By.XPATH, "(//select)[2]")
            dropdown_rate = Select(dropdown_rate_element)
            valor_angular = f"{estrellas - 1}: {estrellas}"
            dropdown_rate.select_by_value(valor_angular)

            self.driver.find_element(By.CLASS_NAME, "btn-add").click()
            print("Juego guardado.")


            xpath_verificacion = f"//h4[contains(@class, 'game-title') and text()='{titulo}']"
            self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_verificacion)))
            print(f"✅ Confirmado: '{titulo}' aparece en la biblioteca.")

        except Exception as e:
            print(f"❌ Error en registro/verificación: {e}")
            self.driver.save_screenshot("fallo_registro.png")

    def scroll_view(self):
        try:
            print("📜 Desplazando hacia la biblioteca de juegos...")

            biblioteca = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "game-grid")))
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", biblioteca)
            
            print("✅ Vista de la biblioteca completada.")
            
            time.sleep(2) 
            self.driver.save_screenshot("coleccion_completa.png")

        except Exception as e:
            print(f"❌ No se pudo desplazar: {e}")

    def delete_duplicate(self):
        try:
            print("🧹 Iniciando limpieza de juegos repetidos con capturas...")
            self.wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "game-card")))
            
            tarjetas = self.driver.find_elements(By.CLASS_NAME, "game-card")
            juegos_cargados = set()
            eliminados = 0

            for i in range(len(tarjetas) - 1, -1, -1):
                tarjetas_actualizadas = self.driver.find_elements(By.CLASS_NAME, "game-card")
                tarjeta = tarjetas_actualizadas[i]
                
                titulo = tarjeta.find_element(By.CLASS_NAME, "game-title").text
                
                if titulo in juegos_cargados:
                    self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", tarjeta)
                    time.sleep(1)
                    
                    nombre_archivo = f"duplicado_{titulo.replace(' ', '_')}.png"
                    self.driver.save_screenshot(nombre_archivo)
                    print(f"📸 Evidencia guardada: {nombre_archivo}")

                    boton_eliminar = tarjeta.find_element(By.CLASS_NAME, "btn-delete-card")
                    self.driver.execute_script("arguments[0].click();", boton_eliminar)

                    try:
                        alerta = self.wait.until(EC.alert_is_present())
                        print(f"⚠️ Alerta detectada: {alerta.text}")
                        alerta.accept()
                        print("✅ Alerta aceptada.")
                    except:
                        print("No se detectó alerta de navegador (quizás es un modal de Angular).")

                    eliminados += 1
                    time.sleep(1.5) 
                else:
                    juegos_cargados.add(titulo)

            print(f"✨ Limpieza terminada. Se eliminaron {eliminados} juegos repetidos.")

        except Exception as e:
            print(f"❌ Error durante la eliminación: {e}")
            self.driver.save_screenshot("error_alerta_eliminacion.png")
    
    def goToStreamlit(self):
        try:
            print("🖱️ Haciendo clic en el botón de Estadísticas...")
            
            btn_stats = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-stats")))
            btn_stats.click()

            time.sleep(3) 
            ventanas = self.driver.window_handles
            self.driver.switch_to.window(ventanas[1])

            url_actual = self.driver.current_url
            titulo_dashboard = self.driver.title
            
            print(f"📍 URL detectada: {url_actual}")
            print(f"📖 Título de la pestaña: {titulo_dashboard}")

            if "8501" in url_actual and "GamerVault" in titulo_dashboard:
                print("✅ ¡PRUEBA EXITOSA! Dashboard cargado.")

                metricas = self.wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "[data-testid='stMetricValue']")))
                
                total = metricas[0].text
                rating = metricas[1].text
                plataforma = metricas[2].text

                #CREACIÓN DEL INFORME TXT
                with open("informe_estadisticas.txt", "w", encoding="utf-8") as f:
                    f.write("=== REPORTE DE AUDITORÍA GAMERVAULT ===\n")
                    f.write(f"Juegos Totales: {total}\n")
                    f.write(f"Rating Promedio: {rating}\n")
                    f.write(f"Plataforma Principal: {plataforma}\n")
                    f.write("=======================================\n")
                
                print("📄 Informe 'informe_estadisticas.txt' generado.")
                self.driver.save_screenshot("evidencia_dashboard_ok.png")

                # 🧹 CERRAR Y VOLVER
                print("🏠 Cerrando pestaña de análisis y volviendo al catálogo...")
                self.driver.close() # Cierra Streamlit
                self.driver.switch_to.window(ventanas[0]) # Regresa a Angular
                
            else:
                print("❌ Error: El Dashboard no coincide con lo esperado.")

        except Exception as e:
            print(f"⚠️ Error en la automatización de estadísticas: {e}")
            self.driver.save_screenshot("error_streamlit.png")


    def cerrar_sesion(self):
        self.driver.find_element(By.CLASS_NAME, "btn-exit").click()
        print("Sesión cerrada.")