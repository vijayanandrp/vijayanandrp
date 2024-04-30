# Greetings

| english                      | tamil                                     | hindi                                      | kannada                                | telugu                                     | malayalam                             |
|------------------------------|-------------------------------------------|--------------------------------------------|----------------------------------------|--------------------------------------------|---------------------------------------|
| Hi                           | Vaṇakkam                                  | namaste                                    | Namaste                                | Hāy                                        | dhikam                                |
| Hello                        | Vaṇakkam                                  | namaste                                    | Namaskāra                              | Halō                                       | halayaa                               |
| How are you?                 | Eppaṭi irukkiṟīrkaḷ?                      | aap kaise hain?                            | Nīvu hēgiddīri?                        | Mīru elā unnāru?                           | sukhamaaneaa?                         |
| Good evening                 | Mālai vaṇakkam                            | shubh sandhya                              | Śubha san̄je                            | Śubha sāyantraṁ                            | gud eevaning                          |
| Afternoon                    | Piṟpakal                                  | dopahar                                    | Madhyāhna                              | Madhyāhnaṁ                                 | uchakazhinju                          |
| Good Morning                 | Kālai vaṇakkam                            | shubh prabhaat                             | Śubhōdaya                              | Śubhōdayaṁ                                 | suprabhaatham                         |
| How do you do                | Nīṅkaḷ eppaṭi ceykiṟīrkaḷ                 | aap kaise hain                             | Nīvu hēge māḍuttīri                    | Elā unnāru                                 | nee enganeyirikkunnu                  |
| Hey                          | Ēy                                        | are                                        | Hē                                     | Hē                                         | hey                                   |
| Pleased to meet you          | Uṅkaḷai cantittatil makiḻcci              | aapase milakar khushee huee                | Nim'mannu bhēṭiyāgi santōṣavāgide      | Mim'malni kalavaḍaṁ ānandaṅgā undi         | ningale kaananaayathil santheaasham   |
| Good to see you              | Uṅkaḷaip pārppatu nallatu                 | aapako dekhakar achchha laga               | Ninna nōḍiddu oḷḷeyadāytu              | Ninni cūsinanduku cāla santōṣaṅgā undi     | ningale kandathil sandosham           |
| Long time no see             | Neṭu nāṭkaḷāka pārkka villai              | bahut dinon se mulaakaat nahin huee        | Dīrghakāla nōḍi                        | Cālā kālaṁ cūḍalēdu                        | deerghanaalaayi kandittu              |
| Alright                      | Cari                                      | theek                                      | Sari                                   | Ālraiṭ                                     | kuzhappam                             |
| Dear Sir or Madam            | Aṉpuḷḷa aiyā allatu am'maiyīr             | priy mahoday ya mahodaya                   | Ātmīya sar athavā mēḍaṁ                | Priyamaina sar lēdā mēḍam                  | priya shreemaan allengil shreemathi   |
| How have you been?           | Nīṅkaḷ eppaṭi iruntīrkaḷ?                 | kya aap?                                   | Nīvu hēgiddīri?                        | Elā unnāvu?                                | ningalkku enganeyundu?                |
| Howdy                        | Eppaṭi                                    | kaise ho                                   | Haud                                   | Hauḍī                                      | houdi                                 |
| Greetings                    | Vāḻttukkaḷ                                | abhivaadan                                 | Śubhāśayagaḷu                          | Śubhākāṅkṣalu                              | aashamsakal                           |
| To Whom it May Concern       | Itu yārukku campantappaṭṭatu              | unake lie jo isase sambaddh ho sakate hain | Idu yārige sambandhisirabahudu         | Evariki idi āndōḷana kaligistundi          | aare udheshichaaneaa avarkku          |
| Allow me to introduce myself | Eṉṉai aṟimukappaṭutta eṉṉai aṉumatikkavum | mujhe apana parichay dene kee anumati den  | Nannannu paricayisalu nanage anumatisi | Nāgurin̄ci ceppukōvaḍāniki avakāsaṁ ivvaṇḍi | enne parichayappeduthaan anuvadikkuka |
| Hello Stranger               | Vaṇakkam anniyaṉē                         | hailo ajanabee                             | Halō sṭrēn̄jar                          | Halō sṭrēn̄jar                              | halo aparichithan                     |
| Bye                          | Varukiṟēṉ                                 | alavida                                    | Bennelubu                              | Bai                                        | bai                                   |
| Good Day                     | Nalla nāḷ                                 | shubh din                                  | Śubha dina                             | Man̄ci rōju                                 | shubhadinam                           |
| Thanks                       | Naṉṟi                                     | dhanyavaad                                 | Dhan'yavādagaḷu                        | Dhan'yavādālu                              | nandi                                 |
| Thank you                    | Naṉṟi                                     | dhanyavaad                                 | Dhan'yavāda                            | Dhan'yavādālu                              | nandi                                 |
| Pleasure                     | Iṉpam                                     | aanand                                     | Santōṣa                                | Ānandaṁ                                    | sandosham                             |



```python
%pip install googletrans==4.0.0rc1 

from googletrans import Translator

translator = Translator(
    service_urls=['translate.google.com', 
                  'translate.google.co.in']
    )

target_language = {'ta': 'tamil', 'hi': 'hindi',  'kn': 'kannada', 'te': 'telugu', 'ml': 'malayalam'}

source = {'en': 'english'}

words = {'greetings': ['Hi', 'Hello', 'How are you?', 'Good evening', 'Afternoon', 
                       'Good Morning', 'How do you do', 'Hey', 'Pleased to meet you',
                       'Good to see you', 'Long time no see', 'Alright', 'Dear Sir or Madam', 
                       'How have you been?', 'Howdy', 'Greetings', 'To Whom it May Concern',
                       'Allow me to introduce myself', 'Hello Stranger', 'Bye', 
                       'Good Day', 'Thanks', 'Thank you', 'Pleasure']
}

translated_dict = {}

for dest in target_language.keys():
  for word in words['greetings']:
    translate = translator.translate(word, src='en', dest=dest)
    if word not in translated_dict:
      translated_dict[word] = []
    translated_dict[word].append((target_language[dest], translate.pronunciation ))
  
revised_dict = []

for key in translated_dict.keys():
  value = dict(translated_dict[key])
  revised_dict.append({**{'english': key}, **value})

import pandas as pd

df = pd.DataFrame(revised_dict)

df

print(df.to_markdown(tablefmt="github", index=False))

```
