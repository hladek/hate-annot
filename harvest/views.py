from django.shortcuts import render
from django.db.models import Count,Sum
from django.shortcuts import redirect
from . import models
from . import forms
import random

# get question with least answers
def question_queue(batch,user_name):
    print(batch)
    questions = models.Question.objects.filter(batch_id=batch.id).annotate(num_annotation=Count("annotation")).order_by("num_annotation")
    goodq = []
    for q in questions:
        # check answers by the user
        print(q)
        isbad = False
        for a in q.annotation_set.all():
            if user_name == a.username:
                isbad = True
        if isbad:
            continue
        goodq.append(q)

    if len(goodq) == 0:
        # Batch is depleted
        return None
    # draw random
    return random.choice(goodq)


def question(request):
    userid = "anonymous"
    if "userid" in request.GET:
        userid = request.GET["userid"]
    # get answer from form
    form = forms.AnswerForm(request.POST)
    answer = None
    if "accept" in request.POST:
        answer = models.Answers.ACCEPT
    elif "reject" in request.POST:
        answer = models.Answers.REJECT
    if answer is not None and form.is_valid():
        hate_level = form.cleaned_data.get("hate_level")
        hate_cathegory = form.cleaned_data.get("hate_cathegory")
        question_id = request.POST["question_id"]
        if answer is not None:
            annotation = models.Annotation(username=userid,question_id=question_id,answer=answer,hate_level=hate_level,hate_cathegory=hate_cathegory)
            annotation.save()
    else:
        print("form invalid")
    form = forms.AnswerForm()
    # get active batch
    batches = models.Batch.objects.filter(status=models.Status.ANNOTATION)
    batch = None
    question = None
    if len(batches) == 0:
        pass
    # TODO no active batch
    else:
        # TODO select batch, batch priority
        batch = batches[0]
        question = question_queue(batch,userid)
        if question is None:
            # batch empty, nothing to do
            pass
    # previous questions


    # annotations in all batches
    prev_questions = models.Batch.objects.raw("SELECT harvest_batch.*,harvest_question.batch_id , count(harvest_annotation.id) as annotation_count FROM harvest_question LEFT JOIN harvest_annotation LEFT JOIN harvest_batch WHERE harvest_annotation.question_id = harvest_question.id AND harvest_annotation.username=%s AND harvest_batch.id = harvest_question.batch_id",[userid])
    #prev_questions = models.Batch.objects.annotate(Count("question__annotation")).filter(question__annotation__username=userid)
    #prev_questions = models.Question.objects.filter(annotation__username=userid).count()
    out = {
        "batch":batch,
        "question":question,
        "form":form,
        "userid": userid,
        "prev_questions": prev_questions,
    }
    return render(request,"harvest/question.html",out)

def start(request):
    form = forms.StartForm(request.POST)
    if form.is_valid():
        userid = form.cleaned_data.get("username")
        return redirect("/harvest/question?userid=" + userid)
    out = {
        "form":form
    }
    return render(request,"harvest/start.html",out)
        


def users(request):
    users = models.Annotation.objects.raw("SELECT DISTINCT username,1 as id FROM harvest_annotation")
    res = []
    for u in users:
        print(u)
        userid = u.username
        print(userid)
        prev_questions = models.Batch.objects.raw("SELECT harvest_batch.name,harvest_question.batch_id as id, count(harvest_annotation.id) as annotation_count FROM harvest_question LEFT JOIN harvest_annotation LEFT JOIN harvest_batch WHERE harvest_annotation.question_id = harvest_question.id AND harvest_annotation.username=%s AND harvest_batch.id = harvest_question.batch_id",[userid])
        res.append({"username":userid,"items":prev_questions})
    out = {
        "users":res
    }
    return render(request,"harvest/users.html",out)

def batch(request):
    batch_id = request.GET["batchid"]
    batch = models.Batch.objects.get(id=batch_id)
    users = models.Annotation.objects.raw("SELECT DISTINCT harvest_annotation.username,1 as id FROM harvest_annotation LEFT JOIN harvest_question WHERE harvest_annotation.question_id = harvest_question.id AND harvest_question.batch_id=%s",[batch_id])
    res = []
    for user in users:
        userid = user.username
        prev_questions = models.Question.objects.raw("SELECT count(harvest_annotation.id) as annotation_count FROM harvest_annotation LEFT JOIN harvest_question WHERE harvest_annotation.username=%s and harvest_question.batch_id=%s",[userid,batch_id])
        # TODO - are there too many rejects?
        # count only accepts...
        res.append({
            "username":userid,
            "count":prev_questions[0].annotation_count
        })
    out = {
        "batch":batch,
        "users": res
    }

def index(request):

    batches = models.Batch.objects.raw("SELECT harvest_batch.name,harvest_batch.status,harvest_batch.description,harvest_question.batch_id as id, count(harvest_annotation.id) as annotation_count FROM harvest_question LEFT JOIN harvest_annotation LEFT JOIN harvest_batch WHERE harvest_question.id = harvest_annotation.question_id AND harvest_question.batch_id = harvest_batch.id")
       #batches = models.Batch.objects.select_related("question").aggregate(Count("question__annotation"))
    for b in batches:
        print(b)
    out = {
        "batches": batches
    }
    
    return render(request,"harvest/index.html",out)
# Create your views here.
