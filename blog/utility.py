from django.db.models.base import ModelStateFieldsCacheDescriptor


class Visability_State:
    pending = 'pending'
    under_review = 'under review'
    approved = 'approved'
    hidden = 'hidden'

taglines = ["This is not your parents’ news site!", 'The only site that allows users to find the truth!', 'Are these news stories true or fake?', "If you can’t tell what the truth is, leave this site now!", 
'This site is for entertainment only!', 'This site allows you to be a reporter!', 'The truth is out there!', 'The place where people come to read, report, or talk about news.']