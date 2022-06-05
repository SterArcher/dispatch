from django import forms
from django.core import validators
from .models import *
from django.utils.translation import gettext_lazy as _
import hashlib

#========================================== USEFUL DATA =================================================================================

# TODO import functions!!!

# tole je trenutno narejeno zelo nepraktično, moram spravit vse pomožne datoteke v en file :)

values = {'dispIdentifiedCA': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'dispProvidedCPRinst': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'gender': [(-1, 'Neznano'), (0, 'Moški'), (1, 'Ženska')], 'witnesses': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Očividci'), (2, 'Ekipa NMP'), (3, 'Očividci & NMP')], 'location': [(-1, 'Neznano'), (1, 'Dom/prebivališče'), (2, 'Delovno mesto'), (3, 'Športni/rekreacijski dogodek'), (4, 'Ulica/avtocesta'), (5, 'Javna zgradba'), (6, 'Varovano stanovanje/dom za ostarele'), (7, 'Učna ustanova'), (8, 'Drugo')], 'bystanderResponse': [(-1, 'Neznano'), (0, 'Očividec ni izvajal TPO'), (1, 'Izveden TPO (Samo stiski prsnega koša)'), (2, 'Izveden TPO (Stiski in umetno dihanje)')], 'bystanderAED': [(-1, 'Neznano'), (0, 'Ni bil uporabljen'), (1, 'AED uporabljen, elektrošok ni izveden'), (2, 'AED uporabljen, elektrošok izveden')], 'deadOnArrival': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'firstMonitoredRhy': [(-1, 'Neznano'), (1, 'VT'), (2, 'VT brez pulza'), (3, 'PEA'), (4, 'Asistola'), (5, 'Bradikardia'), (6, 'AED šok ni smiseln'), (7, 'AED šok smiseln')], 'pathogenesis': [(1, 'Zdravstvena težava'), (2, 'Travma'), (3, 'Predoziranje z drogami'), (4, 'Utopitev'), (5, 'Elektrošok'), (6, 'Zadušitev')], 'independentLiving': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'comorbidities': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'vad': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'cardioverterDefib': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Interni'), (2, 'Eksterni')], 'stemiPresent': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'ttm': [(-1, 'Neznano'), (1, 'Med zastojem'), (2, 'Po-ROSC predbolnišnično'), (3, 'Po-ROSC bolnišnično'), (4, 'Terapevtska hipotermija indicirana, neizvedena'), (5, 'Terapevtska hipotermija ni indicirana')], 'drugs': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Adrenaline'), (2, 'Amiodarone'), (4, 'Vasopressin')], 
'airwayControl': [(-1, 'Neznano'), (0, 'Brez used'), (1, 'Orofaringealna dihalna pot'), (2, 'Supraglotična dihalna pot'), (4, 'Endotrahealni tubus'), (8, 'Kirurška dihalna pot')], 'cprQuality': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'vascularAccess': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Centralna venska'), (2, 'Periferna IV'), (3, 'IO'), (4, 'Endotrahealna')], 'mechanicalCPR': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Naprava za mehanske kompresije prnega koša (Lucas)'), (2, 'Trak za razporeditev sile'), (3, 'Druga mehanska naprava')], 'targetVent': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Samo O2'), (2, 'Samo CO2'), (3, 'O2 & CO2')], 'reperfusionAttempt': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Samo angiografija'), (2, 'PCI'), (4, 'Tromboliza')], 'reperfusionTime': [(-1, 'Neznano'), (1, 'Med zastojem'), (2, 'Znotraj 24 h od ROSC'), (3, 'Po 24 h, a pred odpustom')], 'ecls': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Pred ROSC'), (2, 'Po ROSC')], 'iabp': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'glucose': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'specialistHospital': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'ecg': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'survived': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'rosc': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'SurvivalDischarge30d': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'survivalStatus': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 
'transportToHospital': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'organDonation': [(-1, 'Neznano'), (0, 'Ni donor'), (1, 'Donor')]}

titles = {'caseID': 'UUID primera', 'systemID': 'UUID sistema', 'localID': 'UUID območja', 'dispIdentifiedCA': 'Dispečer je prepoznal prisotnost zastoja srca', 'dispProvidedCPRinst': 'Dispečer je posredoval navodila za TPO', 'age': 'Starost', 'gender': 'Spol', 'witnesses': 'Priče zastoja', 'location': 'Lokacija zastoja', 'bystanderResponse': 'Odziv očividca', 'bystanderResponseTime': 'Začetek izvajanja TPO očividcev', 'bystanderAED': 'Uporaba AED', 'bystanderAEDTime': 'Čas prvega AED šoka očividcev', 'deadOnArrival': 'Mrtvogled', 'firstMonitoredRhy': 'Prvi zaznan ritem', 'pathogenesis': 'Patogeneza', 'independentLiving': 'Samostojno življenje', 'comorbidities': 'Pridružene bolezni', 'vad': 'VAD', 'cardioverterDefib': 'Kardioverter-defibrilator', 'stemiPresent': 'Prisoten STEMI', 'responseTime': 'Odzivni čas', 'defibTime': 'Čas do defibrilacije', 'ttm': 'Terapevtska hipotermija', 'ttmTemp': 'TTM Temperatura', 'drugs': 'Aplicirana zdravila', 'airwayControl': 'Tip nadzora dihalne poti', 'cprQuality': 'Kvaliteta TPO', 'shocks': 'Število elektrošokov', 'drugTimings': 'Čas do aplikacije zdravil', 'vascularAccess': 'Vaskularna pot', 'mechanicalCPR': 'Mehanski stiski prnega koša', 'targetVent': 'Ciljana okisgenacija/ventilacija', 'reperfusionAttempt': 'Poskus reperfuzije', 'reperfusionTime': 'Čas do poskusa reperfuzije', 'ecls': 'ECLS', 'iabp': 'IABP', 'ph': 'pH krvi', 'lactate': 'Laktate', 'glucose': 'Glukoza', 'neuroprognosticTests': 'Število in vrsta nevroprognostičnih testov', 'specialistHospital': 'Tip bolnišnice', 'hospitalVolume': 'Obremenitev bolnišnice', 'ecg': 'EKG z 12 odvodi', 'ecgBLOB': 'EKG datoteka', 'targetBP': 'Ciljano upravljanje krvnega pritiska', 'survived': 'Preživetje', 'rosc': 'ROSC', 'roscTime': 'Čas do ROSC', 'SurvivalDischarge30d': '30-dnevno preživetje ali preživetje do odpusta', 'cpcDischarge': 'Nevrološki izid ob odpustu (CPC)', 'mrsDischarge': 'Nevrološki izid ob odpustu (mRS)', 'survivalStatus': 'Status preživetja', 'transportToHospital': 'Transport v bolnišnico', 'treatmentWithdrawn': 'Zdravljenje prekinjeno (vključno s časom)', 'cod': 'Vzrok smrti', 'organDonation': 'Donacija organov', 'patientReportedOutcome': 'Pacientovo poročilo o izidu', 'qualityOfLife': 'Opredelitev kvalitete življenja (standardizirani vprašalniki, npr. EQ-5D, SF-12)'}

# v form se vpise samo ZD, obcina se doloci samodejno glede na ta slovar ki je bil narejen po https://github.com/SterArcher/OHCA-registry-Slovenia/blob/main/data/population/preb.csv 
ems = {'Ajdovščina': 'ZD Ajdovščina', 'Ankaran/Ancarano': 'ZD Koper', 'Apače': 'ZD Gornja Radgona', 'Beltinci': 'ZD Murska Sobota', 'Benedikt': 'ZD Lenart', 'Bistrica ob Sotli': 'ZD Šmarje pri Jelšah', 'Bled': 'ZD Bled', 'Bloke': 'ZD Cerknica', 'Bohinj': 'ZD Bled', 'Borovnica': 'RP UKCL', 'Bovec': 'ZD Tolmin', 
'Braslovče': 'ZD Žalec', 'Brda': 'ZD Nova Gorica', 'Brežice': 'ZD Brežice', 'Brezovica': 'RP UKCL', 'Cankova': 'ZD Murska Sobota', 'Celje': 'ZD Celje', 'Cerklje na Gorenjskem': 'ZD Kranj', 'Cerknica': 'ZD Cerknica', 'Cerkno': 'ZD Idrija', 'Cerkvenjak': 'ZD Lenart', 'Cirkulane': 'ZD Ptuj', 'Črenšovci': 'ZD Lendava', 'Črna na Koroškem': 'Zdravstveno reševalni center Koroške', 'Črnomelj': 'ZD Črnomelj', 'Destrnik': 'ZD Ptuj', 'Divača': 'ZD Sežana', 'Dobje': 
'ZD Šentjur', 'Dobrepolje': 'RP UKCL', 'Dobrna': 'ZD Celje', 'Dobrova - Polhov Gradec': 'RP UKCL', 'Dobrovnik/Dobronak': 'ZD Lendava', 'Dol pri Ljubljani': 'RP UKCL', 'Dolenjske Toplice': 'ZD Novo mesto', 'Domžale': 'ZD Domžale', 'Dornava': 'ZD Ptuj', 'Dravograd': 'Zdravstveno reševalni center Koroške', 'Duplek': 'ZD Maribor', 'Gorenja vas - Poljane': 'ZD Škofja Loka', 'Gorišnica': 'ZD Ptuj', 'Gorje': 'ZD Bled', 'Gornja Radgona': 'ZD Gornja Radgona', 'Gornji Grad': 'ZSDZ NAZARJE', 'Gornji Petrovci': 'ZD Murska Sobota', 'Grad': 'ZD Murska Sobota', 'Grosuplje': 'RP UKCL', 'Hajdina': 'ZD Ptuj', 'Hoče - Slivnica': 'ZD Maribor', 'Hodoš/Hodos': 'ZD Murska Sobota', 'Horjul': 'RP UKCL', 'Hrastnik': 'ZD Hrastnik', 'Hrpelje - Kozina': 'ZD Sežana', 'Idrija': 'ZD Idrija', 'Ig': 'RP UKCL', 'Ilirska Bistrica': 'ZD Ilirska Bistrica', 'Ivančna Gorica': 'RP UKCL', 'Izola/Isola': 'ZD Izola', 'Jesenice': 'ZD Jesenice', 'Jezersko': 'ZD Kranj', 'Juršinci': 'ZD Ptuj', 'Kamnik': 'ZD Kamnik', 'Kanal': 'ZD Nova Gorica', 'Kidričevo': 'ZD Ptuj', 'Kobarid': 'ZD Tolmin', 'Kobilje': 'ZD Lendava', 'Kočevje': 'ZD Kočevje', 'Komen': 'ZD Sežana', 'Komenda': 'ZD Kamnik', 'Koper/Capodistria': 'ZD Koper', 'Kostanjevica na Krki': 'ZD Krško', 
'Kostel': 'ZD Kočevje', 'Kozje': 'ZD Šmarje pri Jelšah', 'Kranj': 'ZD Kranj', 'Kranjska Gora': 'ZD Jesenice', 'Križevci': 'ZD Ljutomer', 'Krško': 'ZD Krško', 'Kungota': 'ZD Maribor', 'Kuzma': 'ZD Murska Sobota', 'Laško': 'ZD Laško', 'Lenart': 'ZD Lenart', 'Lendava/Lendva': 'ZD Lendava', 'Litija': 'ZD Litija', 'Ljubljana': 'RP UKCL', 'Ljubno': 'ZSDZ NAZARJE', 'Ljutomer': 'ZD Ljutomer', 'Log - Dragomer': 'RP UKCL', 'Logatec': 'ZD Logatec', 'Loška dolina': 'ZD Cerknica', 'Loški Potok': 'ZD Ribnica', 'Lovrenc na Pohorju': 'ZD Maribor', 'Luče': 'ZSDZ NAZARJE', 'Lukovica': 'ZD Domžale', 'Majšperk': 'ZD Ptuj', 'Makole': 'ZD Slovenska Bistrica', 'Maribor': 'ZD Maribor', 'Markovci': 'ZD Ptuj', 'Medvode': 'RP UKCL', 'Mengeš': 'ZD Domžale', 'Metlika': 'ZD Metlika', 
'Mežica': 'Zdravstveno reševalni center Koroške', 'Miklavž na Dravskem polju': 'ZD Maribor', 'Miren - Kostanjevica': 'ZD Nova Gorica', 'Mirna': 'ZD Trebnje', 'Mirna Peč': 'ZD Novo mesto', 'Mislinja': 'Zdravstveno reševalni center Koroške', 'Mokronog - Trebelno': 'ZD Trebnje', 'Moravče': 'ZD Domžale', 'Moravske Toplice': 'ZD Murska Sobota', 'Mozirje': 'ZSDZ NAZARJE', 'Murska Sobota': 'ZD Murska Sobota', 'Muta': 'Zdravstveno reševalni center Koroške', 'Naklo': 'ZD Kranj', 'Nazarje': 'ZSDZ NAZARJE', 'Nova Gorica': 'ZD Nova Gorica', 'Novo mesto': 'ZD Novo mesto', 'Odranci': 'ZD Lendava', 'Oplotnica': 'ZD Slovenska Bistrica', 'Ormož': 'ZD Ormož', 'Osilnica': 'ZD Kočevje', 'Pesnica': 'ZD Maribor', 'Piran/Pirano': 'ZD Koper', 'Pivka': 'ZD Postojna', 'Podčetrtek': 'ZD Šmarje pri Jelšah', 'Podlehnik': 'ZD Ptuj', 'Podvelka': 'Zdravstveno reševalni center Koroške', 'Poljčane': 'ZD Slovenska Bistrica', 'Polzela': 'ZD Žalec', 'Postojna': 'ZD Postojna', 'Prebold': 'ZD Žalec', 'Preddvor': 'ZD Kranj', 'Prevalje': 'Zdravstveno reševalni center Koroške', 'Ptuj': 'ZD Ptuj', 'Puconci': 'ZD Murska Sobota', 'Rače - Fram': 'ZD Maribor', 'Radeče': 'ZD Radeče', 'Radenci': 'ZD Gornja Radgona', 'Radlje ob Dravi': 'Zdravstveno reševalni center Koroške', 'Radovljica': 'ZD Bled', 'Ravne na Koroškem': 'Zdravstveno reševalni center Koroške', 'Razkrižje': 'ZD Ljutomer', 'Rečica ob Savinji': 'ZSDZ NAZARJE', 'Renče - Vogrsko': 'ZD Nova Gorica', 'Ribnica': 'ZD Ribnica', 'Ribnica na Pohorju': 'Zdravstveno reševalni center Koroške', 'Rogaška Slatina': 'ZD Šmarje pri Jelšah', 'Rogašovci': 'ZD Murska Sobota', 'Rogatec': 'ZD Šmarje pri Jelšah', 'Ruše': 'ZD Maribor', 'Šalovci': 'ZD Murska Sobota', 'Selnica ob Dravi': 'ZD Maribor', 'Semič': 'ZD Črnomelj', 'Šempeter - Vrtojba': 'ZD Nova Gorica', 'Šenčur': 'ZD Kranj', 'Šentilj': 'ZD Maribor', 'Šentjernej': 'ZD Novo mesto', 'Šentjur': 'ZD Šentjur', 'Šentrupert': 'ZD Trebnje', 'Sevnica': 'ZD Sevnica', 'Sežana': 'ZD Sežana', 'Škocjan': 'ZD Novo mesto', 'Škofja Loka': 'ZD Škofja Loka', 'Škofljica': 'RP UKCL', 'Slovenj Gradec': 'Zdravstveno reševalni center Koroške', 'Slovenska Bistrica': 'ZD Slovenska Bistrica', 'Slovenske Konjice': 'ZD Slovenske Konjice', 'Šmarje pri Jelšah': 'ZD Šmarje pri Jelšah', 'Šmarješke Toplice': 'ZD Novo mesto', 'Šmartno ob Paki': 'ZD Velenje', 'Šmartno pri Litiji': 'ZD Litija', 'Sodražica': 'ZD Ribnica', 'Solčava': 'ZSDZ NAZARJE', 'Šoštanj': 'ZD Velenje', 'Središče ob Dravi': 
'ZD Ormož', 'Starše': 'ZD Maribor', 'Štore': 'ZD Celje', 'Straža': 'ZD Novo mesto', 'Sveta Ana': 'ZD Lenart', 'Sveta Trojica v Slov. goricah': 'ZD Lenart', 'Sveti Andraž v Slov. goricah': '(prazno)', 'Sveti Jurij ob Ščavnici': 'ZD Gornja Radgona', 'Sveti Jurij v Slov. goricah': 'ZD Lenart', 'Sveti Tomaž': 'ZD Ormož', 'Tabor': 'ZD Žalec', 'Tišina': 'ZD Murska Sobota', 'Tolmin': 'ZD Tolmin', 'Trbovlje': 'ZD Trbovlje', 'Trebnje': 'ZD Trebnje', 'Trnovska vas': 'ZD Ptuj', 'Tržič': 'OZG Gorenjske', 'Trzin': 'ZD Domžale', 'Turnišče': 'ZD Lendava', 'Velenje': 'ZD Velenje', 'Velika Polana': 'ZD Lendava', 'Velike Lašče': 'RP UKCL', 'Veržej': 'ZD Ljutomer', 'Videm': 'ZD Ptuj', 'Vipava': 'ZD Ajdovščina', 'Vitanje': 'ZD Slovenske Konjice', 'Vodice': 'RP UKCL', 'Vojnik': 'ZD Celje', 'Vransko': 'ZD Žalec', 'Vrhnika': 'RP UKCL', 'Vuzenica': 'Zdravstveno reševalni center Koroške', 'Zagorje ob Savi': 'ZD Zagorje', 'Žalec': 'ZD Žalec', 'Zavrč': 'ZD Ptuj', 'Železniki': 'ZD Škofja Loka', 'Žetale': 'ZD Ptuj', 'Žiri': 'ZD Škofja Loka', 'Žirovnica': 'ZD Jesenice', 'Zreče': 'ZD Slovenske Konjice', 'Žužemberk': 'ZD Novo mesto'}

# first form with data immediately after CA
form1 = ['caseID', 'systemID', 'localID', 'dispIdentifiedCA', 'dispProvidedCPRinst', 'age', 'gender', 'witnesses', 'location', 
'bystanderResponse', 'bystanderResponseTime', 'bystanderAED', 'bystanderAEDTime', 'deadOnArrival', 'firstMonitoredRhy', 'pathogenesis', 
'independentLiving', 'comorbidities', 'vad', 'cardioverterDefib', 'stemiPresent', 'responseTime', 'defibTime', 'ttm', 'ttmTemp', 'drugs', 
'airwayControl', 'cprQuality', 'shocks', 'drugTimings', 'vascularAccess', 'mechanicalCPR', 'targetVent', 'reperfusionAttempt', 
'reperfusionTime', 'rosc', 'roscTime', 'transportToHospital', ]

# secodn form with data in the hospital 
form2 = ['caseID', 'systemID', 'localID','ecls', 'iabp', 'ph', 'lactate', 'glucose', 'neuroprognosticTests', 'specialistHospital', 'hospitalVolume', 'ecg', 
'ecgBLOB', 'targetBP', 'survived', 'SurvivalDischarge30d', 'cpcDischarge', 'mrsDischarge', 'survivalStatus', 'treatmentWithdrawn', 
'cod', 'organDonation', 'patientReportedOutcome', 'qualityOfLife']


#======================================== USEFUL FUNCTIONS ==================================================================================


def generate_id(name, surname, cardiac_arrest_date, date_birth):
	"""Takes the name, surname and dates in format 2020-02-03 (year, month, day) and generates ID"""

	# poenotim velike začetnice
	name = name[0].upper() + name[1:].lower()
	surname = surname[0].upper() + surname[1:].lower()

	# split 
	cardiac_arrest_date = cardiac_arrest_date.split("-")
	date_birth = date_birth.split("-")

	ca_date = cardiac_arrest_date[2] + cardiac_arrest_date[1] + cardiac_arrest_date[0]
	birth_date = date_birth[2] + date_birth[1] + date_birth[0]
	
	code = name + ca_date + surname + birth_date
	print(code)
	hashed = hashlib.sha256(code.encode("utf-8")).hexdigest()
	return hashed


def create_widgets(values): 
	w = dict()
	for element in values:
		w[element] = forms.RadioSelect(choices=values[element])#, attrs={"class" : "with-gap", "type" : "radio"}) #attrs={'class': "form-check-input", "type" : "radio"})
		# w[element] = "radio"
	return w 

w = create_widgets(values) #
w["ecgBLOB"] = forms.FileInput(attrs={"class" : "form-control", "type" : "file"})
w["Patient_name"] = forms.TextInput(attrs={"class" : "form-control", "style" : "max-width: 300px;"})
w["drugTimings"] = forms.Textarea(attrs={"class" : "form-control", "style" : "max-width: 500px;"})

# ========================================== FORMS ================================================================================

class MyNewFrom(forms.ModelForm):
	"""def __init__(self, *args, **kwargs):
				super(MyNewFrom, self ).__init__(*args, **kwargs)
				self.fields['Patient name'] = forms.CharField()
				self.fields['Patient surname'] = forms.CharField()
				self.fields["Date of cardiac arrest"] = forms.DateField()"""

	# popravit vrstni red ??????????
	Patient_name = forms.CharField(label="Patient's name")
	Patient_surname = forms.CharField(label="Patient's surname")
	Date = forms.DateField(label='Date of cardiac arrest', widget=forms.SelectDateWidget(years=[x for x in range(2020,2025)]))
	Date_birth = forms.DateField(label='Date of birth', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)]))


	class Meta: 
		model = CaseReport
		## add form fields for caseID

		fields = tuple(form1)#"__all__" 		
		exclude = ("caseID",) # vpišejo občino, ker en ZD lahko pokriva več občin

		widgets = w
		labels = titles

	
class MySecondNewFrom(forms.ModelForm):
	"""def __init__(self, *args, **kwargs):
				super(MyNewFrom, self ).__init__(*args, **kwargs)
				self.fields['Patient name'] = forms.CharField()
				self.fields['Patient surname'] = forms.CharField()
				self.fields["Date of cardiac arrest"] = forms.DateField()"""

	# popravit vrstni red ??????????
	Patient_name = forms.CharField(label="Patient's name")
	Patient_surname = forms.CharField(label="Patient's surname")
	Date = forms.DateField(label='Date of cardiac arrest', widget=forms.SelectDateWidget(years=[x for x in range(2020,2025)]))
	Date_birth = forms.DateField(label='Date of birth', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)]))


	class Meta: 
		model = CaseReport
		## add form fields for caseID

		fields = tuple(form2)#"__all__" 		
		exclude = ("caseID", "systemID",) # vpišejo občino, ker en ZD lahko pokriva več občin

		widgets = w
		labels = titles
		
# nekej na to temo : https://docs.djangoproject.com/en/dev/ref/forms/validation/

form3 = ["Patient_name", "Patient_surname", "Date", "Date_birth"]

# w = {"Patient_name" : }

class MyThirdNewFrom(forms.ModelForm):
	"""def __init__(self, *args, **kwargs):
				super(MyNewFrom, self ).__init__(*args, **kwargs)
				self.fields['Patient name'] = forms.CharField()
				self.fields['Patient surname'] = forms.CharField()
				self.fields["Date of cardiac arrest"] = forms.DateField()"""

	# popravit vrstni red ??????????
	Patient_name = forms.CharField(label="Patient's name")
	Patient_surname = forms.CharField(label="Patient's surname")
	Date = forms.DateField(label='Date of cardiac arrest', widget=forms.SelectDateWidget(years=[x for x in range(2020,2025)]))
	Date_birth = forms.DateField(label='Date of birth', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)]))


	class Meta: 
		model = CaseReport
		## add form fields for caseID

		fields = "__all__" 		
		exclude = ("caseID",) # vpišejo občino, ker en ZD lahko pokriva več občin

		widgets = w
		labels = titles