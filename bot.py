from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
import notifcar


class Scraping:

    def __init__(self):
        self.notify = notifcar.Notificar()
        #self.notify.escucha()
        self.driver = webdriver.Chrome('chromedriver87')
        self.driver.set_window_position(-10000,0)
            
    def surbetFormula(self, data, casa):
        #print(data)
        try:
            for jugador in data:
                jg1Puntos = float(jugador['puntos1'])
                jg2Puntos = float(jugador['puntos2'])
                # Realizo el calculo
                oper = round((1/jg1Puntos) + (1/jg2Puntos), 2)
                porcentaje = round(((1/oper) * 100) - 100, 0)
                if(oper < 1.00):
                    self.notify.mensaje('\U0001F3C6 *{} - {}* \U0001F3C6 \nHay un Surebet para {} puntos: {} vs {} puntos: {} = {}%'.format(
                        casa, jugador['categoria'], jugador['nombre1'], jugador['puntos1'], jugador['nombre2'], jugador['puntos2'], porcentaje))
        except:
            self.notify.mensaje(
                'No se pudo aplicar la formula para {}'.format(casa))

        pass

    def megapuesta(self):
        self.driver.get("https://www.megapuesta.co/#/")
        miLista = []
        try:
            sleep(5)
            menu = self.driver.find_elements_by_xpath(
                '//*[@id="widget-W1J5R5Z0G5A6D4L9L4B0172"]/div/div[2]/div[1]/ul/li')
            cantMenu = len(menu)
            menuID = random.randrange(cantMenu)
            if menuID == 0:
                menuID += 1

            btnMenu = self.driver.find_elements_by_xpath(
                '//*[@id="widget-W1J5R5Z0G5A6D4L9L4B0172"]/div/div[2]/div[1]/ul/li[{}]/a'.format(menuID))[0]
            categoria = btnMenu.get_attribute('innerHTML')
            btnMenu.click()
            sleep(6)
            contenido = self.driver.find_elements_by_xpath(
                '//div[@id="widget-W1J5R5Z0G5A6D4L9L4B0172"]/div/div[2]/div[2]/div')

            for jugadores in contenido:
                try:
                    jug1Nombre = jugadores.find_element_by_xpath(
                        './/*[@class="bto-sb-event-odds-right"]/div[2]/span[1]/i[1]').text
                    jug1Puntos = jugadores.find_element_by_xpath(
                        './/div[@class="bto-sb-event-odds-right"]/div[2]/span[1]/i[2]').text

                    jug2Nombre = jugadores.find_element_by_xpath(
                        './/*[@class="bto-sb-event-odds-right"]/div[2]/span[2]/i[1]').text
                    # print(jug2Nombre)
                    jug2Puntos = jugadores.find_element_by_xpath(
                        './/div[@class="bto-sb-event-odds-right"]/div[2]/span[2]/i[2]').text
                    miLista.append({'categoria': categoria, 'nombre1': jug1Nombre,
                                    'puntos1': jug1Puntos, 'nombre2': jug2Nombre, 'puntos2': jug2Puntos})
                except:
                    print('No se encontraron datos')

        except:
            # print(ValueError)
            print('Error general')
        finally:
            self.surbetFormula(miLista, 'Megapuesta')
            # print(miLista)

    def wplay(self):
        self.driver.get("https://apuestas.wplay.co/es")
        miLista = []
        try:
            sleep(8)
            menu = self.driver.find_elements_by_xpath(
                '//*[@id="main-area"]/div[1]/div/div[1]/ul/li')
            cantMenu = len(menu)
            menuID = random.randrange(cantMenu)
            if menuID == 0:
                menuID += 1
            btnMenu = self.driver.find_elements_by_xpath(
                '//*[@id="main-area"]/div[1]/div/div[1]/ul/li[{}]/a'.format(menuID))[0]
            categoria = btnMenu.get_attribute('innerHTML').replace(
                '\n', '').replace('<span>', '').replace('</span>', '')
            # obtengo el id del DIV
            idDiv = btnMenu.get_attribute('href')
            idDiv = idDiv.split('/')[3].split('#')[1]
            btnMenu.click()
            sleep(3)
            # //*[@id="inplay-tab-BASK"]/div/div[2]/div[1]
            contenido = self.driver.find_elements_by_xpath(
                '//*[@id="{}"]/div/div[2]/div/div/div'.format(idDiv))

            for jugadores in contenido:
                try:
                    # print(jugadores.get_attribute('innerHTML'))
                    jug1Nombre = jugadores.find_element_by_xpath(
                        './/div[5]/table/tbody/tr/td[1]/div/button/span/span[2]/span/span').text
                    jug1Puntos = jugadores.find_element_by_xpath(
                        './/div[5]/table/tbody/tr/td[1]/div/button/span/span[4]').text
                    jug2Nombre = jugadores.find_element_by_xpath(
                        './/div[5]/table/tbody/tr/td[2]/div/button/span/span[2]/span/span').text
                    jug2Puntos = jugadores.find_element_by_xpath(
                        './/div[5]/table/tbody/tr/td[2]/div/button/span/span[4]').text
                    miLista.append({'categoria': categoria, 'nombre1': jug1Nombre,
                                    'puntos1': jug1Puntos, 'nombre2': jug2Nombre, 'puntos2': jug2Puntos})
                except:
                    print('No se encontraron datos')

        except:
            # print(ValueError)
            print('Error general')
        finally:
            self.surbetFormula(miLista, 'Wplay')

    def rushbet(self):
        linksMenu = [
            {'categoria': "tennis", 'url': "https://www.rushbet.co/#filter/tennis"},
            {
                'categoria': "table_tennis",
                'url': "https://www.rushbet.co/#filter/table_tennis",
            },
            {
                'categoria': "basketball",
                'url': "https://www.rushbet.co/#filter/basketball",
            },
            {
                'categoria': "volleyball",
                'url': "https://www.rushbet.co/#filter/volleyball",
            },
            {'categoria': "baseball", 'url': "https://www.rushbet.co/#filter/baseball"},
            {'categoria': "handball", 'url': "https://www.rushbet.co/#filter/handball"},
            {'categoria': "darts", 'url': "https://www.rushbet.co/#filter/darts"}]
        index = random.randrange(len(linksMenu))
        self.driver.get(linksMenu[index]['url'])
        miLista = []
        try:
            categoria = linksMenu[index]['categoria']
            sleep(4)
            contenido = self.driver.find_elements_by_xpath(
                '//*[@id="KambiBC-content"]/div/div/div/div[4]/div[1]/div/div[3]/div[2]/div/div/div[3]/div/ul/li')

            for jugadores in contenido:
                try:
                    jug1Nombre = jugadores.find_element_by_xpath(
                        './/div[@class="KambiBC-bet-offer__outcomes"]/button[1]/div/div[1]').text
                    jug1Puntos = jugadores.find_element_by_xpath(
                        './/div[@class="KambiBC-bet-offer__outcomes"]/button[1]/div/div[2]').text

                    jug2Nombre = jugadores.find_element_by_xpath(
                        './/div[@class="KambiBC-bet-offer__outcomes"]/button[2]/div/div[1]').text
                    jug2Puntos = jugadores.find_element_by_xpath(
                        './/div[@class="KambiBC-bet-offer__outcomes"]/button[2]/div/div[2]').text

                    if jug2Nombre == 'Empate':
                        jug2Nombre = jugadores.find_element_by_xpath(
                            './/div[@class="KambiBC-bet-offer__outcomes"]/button[3]/div/div[1]').text
                        jug2Puntos = jugadores.find_element_by_xpath(
                            './/div[@class="KambiBC-bet-offer__outcomes"]/button[3]/div/div[2]').text

                    miLista.append({'categoria': categoria, 'nombre1': jug1Nombre,
                                    'puntos1': jug1Puntos, 'nombre2': jug2Nombre, 'puntos2': jug2Puntos})
                except:
                    print('No se encontraron datos')
        except:
            # print(ValueError)
            print('Error general')
        finally:
            self.surbetFormula(miLista, 'Rushbet')
            # print(miLista)

    def yajuegos(self):
        self.driver.get("https://sports.yajuego.co")
        miLista = []
        try:
            sleep(8)
            menu = self.driver.find_elements_by_xpath('//*[@id="wrapper"]/main/div/div/div/div[2]/div/div[2]/div/div[2]/div/nav/div/div/ul/li')
            cantMenu = len(menu)
            menuID = random.randrange(cantMenu)
            if menuID == 0:
                menuID += 1

            btnMenu = self.driver.find_elements_by_xpath(
                '//*[@id="wrapper"]/main/div/div/div/div[2]/div/div[2]/div/div[2]/div/nav/div/div/ul/li[{}]'.format(menuID))[0]
            categoria = btnMenu.find_element_by_xpath('.//span').text
            print(categoria)
            btnMenu.click()
            sleep(5)
            contenido = self.driver.find_elements_by_xpath('//*[@id="wrapper"]/main/div/div/div/div[2]/div/div[2]/div/div[2]/div/div[3]/div')

            for jugadores in contenido:
                try:
                    jug1Nombre = jugadores.find_element_by_xpath('.//div[2]/div[1]').text
                    jug1Puntos = jugadores.find_element_by_xpath('.//div[6]/ul/li[1]').text

                    jug2Nombre = jugadores.find_element_by_xpath('.//div[2]/div[2]').text
                    jug2Puntos = jugadores.find_element_by_xpath('.//div[6]/ul/li[2]').text
                    
                    miLista.append({'categoria': categoria, 'nombre1': jug1Nombre,
                                    'puntos1': jug1Puntos, 'nombre2': jug2Nombre, 'puntos2': jug2Puntos})
                except:
                    print('No se encontraron datos')
        except:
            print('Error general')
        finally:
            self.surbetFormula(miLista, 'Megapuesta')

    def finalizarSession(self):
        self.driver.close()

# BLOQUE PRINCIPAL
scraping = Scraping()
while True:
    scraping.megapuesta()
    scraping.wplay()
    scraping.rushbet()
    scraping.yajuegos()
scraping.finalizarSession()
