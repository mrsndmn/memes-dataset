
from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm.auto import tqdm

# https://imgflip.com/memetemplates

dataset = []
imgflip_base_url = 'https://imgflip.com'
template_names = [
                  '216523697/All-My-Homies-Hate',
                  'Drake-Hotline-Bling',
                  'Two-Buttons',
                  'Distracted-Boyfriend',
                  'Buff-Doge-vs-Cheems',
                  'Expanding-Brain',
                  'Epic-Handshake',
                  'Disaster-Girl',
                  'Woman-Yelling-At-Cat',
                  '221578498/Grant-Gustin-over-grave',
                  '50421420/Disappointed-Black-Guy',
                  'Monkey-Puppet',
                  'I-Bet-Hes-Thinking-About-Other-Women',
                  '322841258/Anakin-Padme-4-Panel',
                  'X-X-Everywhere',
                  '195710097/Black-guy-hiding-behind-tree',
                  'Hide-the-Pain-Harold',
                  '309868304/Trade-Offer',
                  'Bike-Fall',
                  'Roll-Safe-Think-About-It',
                  'Ancient-Aliens',
                  'This-Is-Fine',
                  '167991076/Skyrim-skill-meme',
                  'Success-Kid',
                  '342785297/Gus-Fring-we-are-not-the-same',
                  'Third-World-Skeptical-Kid',
                  'Unsettled-Tom',
                  'Leonardo-Dicaprio-Cheers',
                  'Futurama-Fry',
                  '110133729/spiderman-pointing-at-spiderman',
                  '238694077/Knight-with-arrow-in-helmet',
                  'Always-Has-Been',
                  'Is-This-A-Pigeon',
                  '193286698/Empty-Stonks',
                  '188789496/Moe-throws-Barney',
                  'Bender',
                  'Shut-Up-And-Take-My-Money-Fry',
                  '133946291/You-know-Im-something-of-a-scientist-myself',
                  '211387869/Black-Scientist-Finally-Xium',
                  '136840273/laughing-kid',
                  'Evil-Toddler',
                  '113387478/The-Cooler-Daniel',
                  '85552183/skinner-pathetic',
                ]

try:
    template_names = set(template_names)

    print('templates to process:', len(template_names))

    MAX_TEMPLATE_PAGES = 100

    for template_name in sorted(template_names):
        for template_page_num in range(1, MAX_TEMPLATE_PAGES):
            drake_memes_req = requests.get(imgflip_base_url + '/meme/' + template_name + "?page=" + str(template_page_num) )

            if drake_memes_req.status_code != 200:
                print("drake_memes_req.status_code:", drake_memes_req.status_code)
                break

            drake_memes = BeautifulSoup(drake_memes_req.content, 'html.parser')
            memes = drake_memes.find_all('h2', attrs={'class': 'base-unit-title'})

            for mem in tqdm(memes):
                specific_mem = mem.find_next('a')
                specific_mem_href = specific_mem.get('href')
                specific_mem_page = requests.get(imgflip_base_url + specific_mem_href)
                if specific_mem_page.status_code != 200:
                    print("oops error getting:", specific_mem_href)
                    continue

                specific_mem_bs = BeautifulSoup(specific_mem_page.content, 'html.parser')
                mem_description = ''
                try:
                    mem_description = specific_mem_bs.find_all('div', attrs={ "class": "img-desc" })[0].text
                except Exception as e:
                    print("error parse", specific_mem_href, "err:", e)

                dataset.append({
                    'template': template_name,
                    'mem_href': specific_mem_href,
                    'mem_description': mem_description,
                })

    len(dataset)

except Exception as e:
    print("global exception:", e)

df = pd.DataFrame(dataset)
df

df.to_csv('memes-dataset.csv', index=False)

