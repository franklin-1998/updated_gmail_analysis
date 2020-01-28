# try:
                #     body_reading = BeautifulSoup(each_mes['body']['content'], 'html.parser')
                #     elements = body_reading.find_all("div", id="Signature")
                #     for element in elements:
                #         element.decompose()
                #     body_content = body_reading.get_text().encode("ascii", "ignore").decode("utf-8")
                #     body_content = re.sub(r'(\n\s*)+\n+', '\n\n', body_content)
                #     text, signatures = signature.extract(body_content,sender=each_mes['from']['emailAddress']['address'])
                #     text1, signatures1 = signature.extract(text,sender=each_mes['from']['emailAddress']['address'])
                #     text2, signatures2 = signature.extract(signatures,sender=each_mes['from']['emailAddress']['address'])
                #     Body.append(re.sub("None","",(str(text1)+str(text2))))
                # except TypeError:
                #     body_reading = BeautifulSoup(each_mes['body']['content'], 'html.parser')
                #     elements = body_reading.find_all("div", id="Signature")
                #     for element in elements:
                #         element.decompose()
                #     body_content = body_reading.get_text().encode("ascii", "ignore").decode("utf-8")
                #     body_content = re.sub(r'(\n\s*)+\n+', '\n\n', body_content)
                #     Body.append(body_content)