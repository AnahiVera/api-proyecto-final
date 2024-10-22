from app import app
from models import Rank, Technology, Language, Status


with app.app_context():
    status7 = Status()
    status7.name='Private'
    status7.save()
"""    
    status4 = Status()
    status4.name='Pending'
    status4.save()

    status5 = Status()
    status5.name='Rejected'
    status5.save()
    
    status6 = Status()
    status6.name='Accepted'
    status6.save()

    lang1 = Language()
    lang1.name='Spanish'
    lang1.save()

    lang2 = Language()
    lang2.name='Korean'
    lang2.save()

    lang3 = Language()
    lang3.name='English'
    lang3.save()


    rank1 = Rank()
    rank1.name='Junior'
    rank1.save()
    
    rank2 = Rank()
    rank2.name='Semi-Senior'
    rank2.save()
    
    rank3 = Rank()
    rank3.name='Senior'
    rank3.save()
    

    status1 = Status()
    status1.name='Public'
    status1.save()

    status2 = Status()
    status2.name='Completed'
    status2.save()

    status3 = Status()
    status3.name='In process'
    status3.save()

    technologies1 = Technology()
    technologies1.name='Java'
    technologies1.save()

    technologies2 = Technology()
    technologies2.name='Javascript'
    technologies2.save()

    technologies3 = Technology()
    technologies3.name='Python'
    technologies3.save()

    technologies4 = Technology()
    technologies4.name='SQL'
    technologies4.save()

    technologies5 = Technology()
    technologies5.name='React'
    technologies5.save()

    technologies6 = Technology()
    technologies6.name='CSS'
    technologies6.save()

    technologies7 = Technology()
    technologies7.name='GO'
    technologies7.save()

    technologies8 = Technology()
    technologies8.name='Bootstrap'
    technologies8.save()

    technologies9 = Technology()
    technologies9.name='NodeJS'
    technologies9.save()
 """