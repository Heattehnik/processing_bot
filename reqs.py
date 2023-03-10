import requests


json_string = {
  "headers": {
    "accept": "*/*",
    "accept-language": "ru,en;q=0.9",
    "content-type": "multipart/form-data; boundary=----WebKitFormBoundaryEgwnCnYt6VYRDjq7",
    "sec-ch-ua": "\"Not?A_Brand\";v=\"8\", \"Chromium\";v=\"108\", \"Yandex\";v=\"23\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin"
  },
  "referrer": "https://support.fsa.gov.ru/",
  "referrerPolicy": "strict-origin-when-cross-origin",
  "body": "------WebKitFormBoundaryEgwnCnYt6VYRDjq7\r\nContent-Disposition: form-data; name=\"alType\"\r\n\r\nmeasurements\r\n------WebKitFormBoundaryEgwnCnYt6VYRDjq7\r\nContent-Disposition: form-data; name=\"alNumber\"\r\n\r\nRA.RU.320019\r\n------WebKitFormBoundaryEgwnCnYt6VYRDjq7\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\nalexdyachenko@mail.ru\r\n------WebKitFormBoundaryEgwnCnYt6VYRDjq7\r\nContent-Disposition: form-data; name=\"reportFields\"\r\n\r\n{\"checkNumber\":\"16078-13\",\"checkDate\":\"2023-02-12\",\"limitation\":\"6\",\"measurementType\":\"СГВ-15\",\"measurementResult\":\"Пригодно\",\"verificatorSecondName\":\"Пономарёв\",\"verificatorName\":\"Никита\",\"verificatorPatronymic\":\"Михайлович\"}\r\n------WebKitFormBoundaryEgwnCnYt6VYRDjq7--\r\n",
  "method": "POST",
  "mode": "cors",
  "credentials": "include"
}

request = requests.post('https://support.fsa.gov.ru/api/reports/metrology', json=json_string)

print(request.text)
