from app import app
from models import Rank, Technologies, Language, Status


with app.app_context():

    lang1= Language()
    lang1.name='Spanish'
    lang1.save()

    lang2= Language()
    lang2.name='Korean'
    lang2.save()

    lang3= Language()
    lang3.name='English'
    lang3.save()


    rank1= Rank()
    rank1.name='Junior'
    rank1.save()

    
    rank2= Rank()
    rank2.name='Semi-Senior'
    rank2.save()

    
    rank3= Rank()
    rank3.name='Senior'
    rank3.save()

    status1= Status()
    status1.name='Public'
    status1.save()

    status2= Status()
    status2.name='Completed'
    status2.save()

    technologies1= Technologies()
    technologies1.name='Java'
    technologies1.save()

    technologies2= Technologies()
    technologies2.name='Javascript'
    technologies2.save()

    technologies3= Technologies()
    technologies3.name='Python'
    technologies3.save()

    technologies4= Technologies()
    technologies4.name='SQL'
    technologies4.save()

    technologies5= Technologies()
    technologies5.name='React'
    technologies5.save()

    technologies6= Technologies()
    technologies6.name='CSS'
    technologies6.save()

    technologies7= Technologies()
    technologies7.name='GO'
    technologies7.save()

    technologies8= Technologies()
    technologies8.name='Bootstrap'
    technologies8.save()

    technologies9= Technologies()
    technologies9.name='NodeJS'
    technologies9.save()