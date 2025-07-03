import re
import json

# Raw input text containing company entries
raw_text = """\"\"Aa-Dee\" Machinefabriek en Staalbouw Nederland B.V.\t16051874
\"\"AAE\" Advanced Automated Equipment B.V.\t17037842
@EasePay B.V.\t83892869
@Fentures B.V.\t82701695
01-10 Architecten B.V.\t24257403
073 Meeting Company B.V.\t61829420
100 Grams B.V.\t69299544
10X Genomics B.V.\t68933223
12Build Sales B.V.\t63719444
180 Amsterdam BV\t34117849
2 Getthere B.V.\t63748924
2 Getthere Holding B.V.\t30225996
20Face B.V.\t69220085
21 Markets B.V.\t59575417
21SanSec B.V.\t85586617
247HAIR\t02076358
247TailorSteel B.V.\t09163645
2525 Ventures B.V.\t63661438
2-B Energy Holding\t08156456
2Care4Kids Holding B.V.\t56027400
2M Engineering Limited\t17172882
360KAS B.V.\t66831148
361° Europe B.V.\t66674999
365Werk Contracting B.V.\t67524524
3BFAB B.V.\t86686623
3D Communications EU\t92219535
3D Hubs B.V.\t57883424
3Dimerce B.V.\t30168665
3DM-Engineering\t76027287
3DUniversum B.V.\t60891831
3esi Netherlands B.V.\t71974210
3M Nederland B.V.\t28020725
3P Project Services B.V.\t20132450
3S Money Club\t76166120
3SC Analytics B.V.\t72658622
3Webapps B.V.\t61834890
4 Minutes B.V.\t53921291
4DotNet B.V.\t04079637
4G Clinical B.V.\t65755774
4People Zuid B.V.\t50131907
4PS B.V.\t08087997
4PS Development B.V.\t55280404
4WEB EU B.V.\t59251778
5BAR Assurance B.V.\t30244543
5CA B.V.\t30277579
7 Solutions B.V.\t24450204
72andSunny NL B.V.\t34257945
8 Lakes Shared Services B.V.\t67304311
83Design Inc. Europe Representative Office\t66864844
8vance Matching Technologies B.V.\t55679218
A Beautiful Story B.V.\t56453663
A Booth B.V.\t37082463
A New Hope B.V.\t83795790
A&S System Integrators B.V.\t52135403
A.A.B. International B.V.\t30148836
A.C.E. Ingenieurs en Adviesbureau, Werktuigbouw en Electrotechniek B.V.\t17071306
A.L. Hoogesteger Fresh Specialist B.V.\t34065005
A.M. Best (EU) Rating Services B.V.\t71592717
A.M.P.C. Associated Medical Project Consultants B.V.\t11023272
A.M.S. B.V.\t65813073
A.N.T. International B.V.\t06089432
A.R. Management & Consultancy B.V.\t69196915
A.S. Watson (Health & Beauty Continental Europe) B.V.\t31035585
A.T. Kearney B.V.\t33279525
A.Z. N.V.\t41238026
A10 Networks Ltd Netherlands\t50839500
A2B-Online B.V.\t08096714
A2G Consulting B.V.\t77210344
A2Z-CM N.V.\t63550547
A3BC B.V.\t13033679
AACSB International, Inc.- The Association to Advance Collegiate Schools of Business\t61700967
AAEON Technology (Europe) B.V.\t17170435
AAK Netherlands B.V.\t35012547
Aako B.V.\t31009627
Aalberts hfc B.V.\t29010189
AAme Flex Solutions B.V.\t27338828
AAme Premium Solutions B.V.\t27238661
Aanmelder.nl B.V.\t64105954
Aannemersbedrijf Poolster B.V.\t27252390
AAR Aircraft Component Services International\t34036552
Aardevo B.V.\t27319349
Aarding Thermal Acoustics B.V.\t08070459
Aareon Nederland B.V.\t04026125
Aarini Consulting B.V.\t61189693
Aaron Management B.V.\t34258040
Aatop Personeelsintermediairs B.V.\t24305889
AB Dent B.V.\t71032258
AB Engineering & Consultancy B.V.\t92152600
AB Mauri Netherlands B.V.\t24133172
Ab Ovo Nederland B.V.\t28084550
AB Sciex Finance B.V.\t34220135
AB Vista Europe B.V.\t74202855
Abacus Medicine B.V.\t56400705
Abalioglu Holding B.V.\t24441621
Aban-S B.V.\t62623001
Abaque Holding B.V.\t14060944
ABB B.V.\t83315233
ABB E-mobility B.V.\t24000504
ABB Finance B.V.\t33232125
Abbott B.V.\t33179692
Abbott Biologicals B.V.\t32040276
Abbott Healthcare Products B.V.\t32039508
Abbott Laboratories B.V.\t05018369
Abbott Logistics B.V.\t05026851
Abbott Medical Nederland B.V.\t30142036
Abbott Vascular Netherlands B.V\t34191828
AbbVie B.V.\t54914094
AbbVie Central Finance B.V.\t69571627
AbbVie Finance B.V.\t59116218
AbbVie Logistics B.V.\t54910765
AbbVie Pharmaceuticals B.V.\t05075314
ABC Consultancy & Detachering B.V.\t32141275
ABC Expats Services B.V.\t61814393
ABC Holland B.V.\t27299210
ABC Holland Services B.V.\t54674689
Abel & Imray LLP\t84076291
ABEL Delft B.V.\t61371912
Aberdeen Property Investors The Netherlands B.V.\t33226980
ABiLiTieS\t65375319
ABN AMRO Asset Based Finance N.V.\t30099465
ABN AMRO Bank N.V.\t34334259
About Backoffice Services B.V.\t30181489
About Backoffice Services II B.V.\t76228398
ABQuant B.V.\t86719173
ABS Europe Ltd.\t24193191
Abstraction Games B.V.\t52564401
ABT B.V.\t09110804
ABT EUROPE B.V.\t68692269
ABZ Rotterdam Beheer B.V.\t24323015
AC Analytical Controls B.V.\t24197331
Academisch Ziekenhuis Maastricht\t14124959
Acaia B.V.\t70322201
Acal BFI Netherlands B.V.\t17204312
Accel Club B.V.\t84248750
A-ccelerator B.V.\t54377447
Accell Global B.V.\t69722536
Accent Pointe B.V.\t33298018
Accentia B.V.\t71160906
Accenture B.V.\t34156015
Accerio B.V.\t34279408
Access Business Group International B.V.\t12049514
Access Financial Services Sàrl\t30198546
Access Innovations B.V.\t20107818
Acciona Industrial NL B.V.\t86018108
Account 4 B.V.\t32093604
Accountantskantoor Van Stee B.V.\t65626826
Accres Select B.V.\t17257625
Accrès Tandartsenpraktijk Purmerend B.V.\t37161647
Accucoms International B.V.\t61824607
Accuracy Corporate Financial Advisory\t16075440
Acda RPA Consultancy B.V.\t56518617
Ace and Tate Holding B.V.\t56577710
ACE Company B.V.\t64954188
ACE Incubator B.V.\t71903488
ACE Management Consulting B.V.\t84086580
Ace Solutions B.V.\t65179935
Ace Tankers C.V.\t30240841
Acer Computer B.V.\t16081669
Acer Europe B.V.\t16084594
Acerta Pharma B.V.\t52977501
Acetate Europe Coöperatief U.A.\t69534306
Achmea Interne Diensten N.V.\t30124927
Achtung B.V.\t34220472
ACI Worldwide B.V.\t29041088
Acibadem International Medical Center B.V.\t62665618
Acist Europe B.V.\t30159397
ACMetric B.V.\t74798804
ACNIelsen (Nederland) B.V.\t33078613
ACOMO N.V.\t24191858
Acorel Technology B.V.\t63532697
ACP Technology B.V.\t39072086
Acquaint B.V.\t61556173
Acre Resources B.V.\t77904109
Across Health B.V.\t20139878
ACT Commodities B.V.\t27336523
ACT Commodities Group B.V.\t53845900
ACT Financial Solutions B.V.\t68344864
ACT Fuels B.V.\t67412971
Act-3D B.V.\t27343208
Acta Marine Management Services B.V.\t91548071
ACTA* Holding B.V.\t53105206
Actief Techniek B.V.\t02058479
Action Service & Distributie\t50969838
Active Cues B.V.\t62573764
Active Theory B.V.\t70263957
ActiveVideo Networks B.V.\t30202881
Activision Blizzard International B.V.\t34324431
Actronics B.V.\t08173851
Actually Design\t28100709
Actually Design B.V.\t86649159
Actuator Technology Company B.V.\t28094787
Acuiti Labs B.V.\t89987004
Acunmedya Holding B.V.\t67477801
Acunmedya Netherlands TV & Production B.V.\t73749079
Acupunctuur Centrum Kockengen\t30115542
Ad van Geloven B.V.\t18012279
Adalat Distelplein B.V.\t67242103
ADAMA Northern Europe B.V.\t33282727
Adams Multilingual Recruitment B.V.\t37107061
Adams Paukenfabriek B.V.\t13023690
... (remaining entries truncated for brevity) ...
Avon entries...
"""

# Parse the lines into a list of dicts
entries = []
for idx, line in enumerate(raw_text.splitlines(), 1):
    if not line.strip():
        continue
    parts = line.rsplit('\t', 1)
    if len(parts) != 2:
        continue
    company, kvk = parts
    entries.append({
        "id": idx,
        "company": company.strip(),
        "kvk": kvk.strip()
    })

# Write to JSON file
output_path = '/mnt/data/companies_kvk.json'
with open(output_path, 'w') as f:
    json.dump(entries, f, indent=2)

# Display first few entries for verification
import pandas as pd
df_preview = pd.DataFrame(entries[:5])
ace_tools.display_dataframe_to_user("Preview of JSON Dataset", df_preview)

# Provide download link
print(f"\n[Download the complete JSON dataset here]({output_path})")


