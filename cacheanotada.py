#!/usr/bin/python3

import webapp
import urllib.request


class cacheApp (webapp.webApp):

    cache = {}

    def parse(self, request):
        lista = request.split()
        metodo = lista[0]
        recurso = lista[1][1:]
        return (metodo, recurso)

    def process(self, analiza):

        metodo, recurso = analiza

        if metodo == "GET":
            print(recurso)
            if recurso.split("/")[0] == "reload":
                url = recurso.split("/")[1]
                url = "http://" + url
                httpCode = "302"
                htmlBody = ("<meta http-equiv='refresh' content=3;url=" +
                            url + ">")
            else:
                try:
                    if recurso in self.cache:
                        httpCode = "200 OK"
                        htmlBody = self.cache[recurso]
                    else:
                        url = "http://" + recurso
                        f = urllib.request.urlopen(url)
                        cuerpo = f.read().decode('utf-8')
                        self.cache[recurso] = cuerpo
                        antes = cuerpo.find("<body")
                        despues = cuerpo.find(">", antes)
                        links = ("<a href=" + url + ">Página original</a>" +
                                   "<a href=/reload/" + recurso +
                                   "> Reload </a>")
                        httpCode = "200 OK"
                        htmlBody = (cuerpo[:despues + 1] + links +
                                    cuerpo[despues + 1:])
                except urllib.error.URLError:
                    httpCode = "404 Not Found"
                    htmlBody = "No se ha introducido ninguna URL"
                except UnicodeDecodeError:
                    httpCode = "404 Not Found"
                    htmlBody = "Error al decodificar"
        else:
            httpCode = "HTTP/1.1 405 Method Not Allowed"
            hmtlBody = "Metodo distinto de GET."

        return (httpCode, htmlBody)

if __name__ == "__main__":
        testWebApp = cacheApp("localhost", 1234)
