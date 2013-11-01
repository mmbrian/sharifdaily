from django.http import HttpResponse
# from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from .models import *
from sharifdaily.accounts.views import REAL_SECRET_KEY
from sharifdaily.accounts.utils import diff

try:
    import json
except ImportError:
   from django.utils import simplejson as json

ARTICLES_PER_PAGE = 50
ARCHIVES_PER_PAGE = 50
REPORTS_PER_PAGE = 50
COMMENTS_PER_PAGE = 50

def get_articles(request, page):
	article_list = Article.objects.filter(published = True).values('id', 'date', 'headline', 'content', 'view_count', 'photo').order_by('-date')
	page = int(page)
	start = (page - 1) * ARTICLES_PER_PAGE
	end = page * ARTICLES_PER_PAGE
	return HttpResponse(json.dumps(list(article_list[start:end]), cls=DjangoJSONEncoder))

def get_article_photo_thumbnail(request, _id):
	try:
		article = Article.objects.get(id=_id)
		return HttpResponse(article.photo_thumbnail.url)
	except Article.DoesNotExist:
		return HttpResponse('invalid')

def get_main_archives(request, page):
	return get_archives(request, page, True)
def get_other_archives(request, page):
	return get_archives(request, page, False)
def get_archives(request, page, is_main):
	archive_list = Archive.objects.filter(Q(tag='') if is_main else ~Q(tag='')).values('id', 'tag', 'date', 'title', 'pdf').order_by('-date')
	page = int(page)
	start = (page - 1) * ARCHIVES_PER_PAGE
	end = page * ARCHIVES_PER_PAGE
	return HttpResponse(json.dumps(list(archive_list[start:end]), cls=DjangoJSONEncoder))



def get_reports(request, page):
	report_list = Report.objects.filter(published = True).values('id', 'date', 'headline', 'view_count', 'author', 'tag', 'content', 'photo', 'audio', 'video').order_by('-date')
	page = int(page)
	start = (page - 1) * REPORTS_PER_PAGE
	end = page * REPORTS_PER_PAGE
	return HttpResponse(json.dumps(list(report_list[start:end]), cls=DjangoJSONEncoder))	

def get_article_comments(request, page, _id):
	try:
		comment_list = ArticleComment.objects.filter(article__id=int(_id), is_public=True).values('created', 'tag', 'content').order_by('-created')	
		page_num = int(page)
		start = (page_num - 1) * COMMENTS_PER_PAGE
		end = page_num * COMMENTS_PER_PAGE
		return HttpResponse(json.dumps(list(comment_list[start:end]), cls=DjangoJSONEncoder))	
	except Article.DoesNotExist:
		return HttpResponse('invalid article')		

def get_report_comments(request, page, _id):
	try:
		comment_list = ReportComment.objects.filter(report__id=int(_id), is_public=True).values('created', 'tag', 'content').order_by('-created')	
		page_num = int(page)
		start = (page_num - 1) * COMMENTS_PER_PAGE
		end = page_num * COMMENTS_PER_PAGE
		return HttpResponse(json.dumps(list(comment_list[start:end]), cls=DjangoJSONEncoder))	
	except Report.DoesNotExist:
		return HttpResponse('invalid report')	

def get_article_likes(request, _id):
	return get_likes(Article, int(_id))
def get_report_likes(request, _id):
	return get_likes(Report, int(_id))
def get_likes(model, _id):
	try:
		obj = model.objects.get(id=_id)
		return HttpResponse(str(obj.likes.count()))
	except model.DoesNotExist:
		return HttpResponse('0')

def get_article_likes_and_thumbnail(request, _id):
	try:
		article = Article.objects.get(id=_id)
		return HttpResponse(str(article.likes.count()) +'|'+ article.photo_thumbnail.url)
	except Article.DoesNotExist:
		return HttpResponse('0|')

def has_liked_article(request, user_id, article_id):
	try:
		ret = Like.objects.filter(user__id=int(user_id), article__id=int(article_id)).count()
		return HttpResponse(str(ret))
	except Exception:
		return HttpResponse('0')

def has_liked_report(request, user_id, report_id):
	try:
		ret = Like.objects.filter(user__id=int(user_id), report__id=int(report_id)).count()
		return HttpResponse(str(ret))
	except Exception:
		return HttpResponse('0')

@csrf_exempt
def post_article_comment(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			author_id = request.POST['author_id']
			article_id = request.POST['article_id']
			content = request.POST['content']
			try:
				user = User.objects.get(id=author_id)
				article = Article.objects.get(id=article_id)
				comment = ArticleComment(author=user, article=article, content=content)
				comment.tag = user.get_full_name()
				comment.save()
				return HttpResponse(str(comment.id))
			except User.DoesNotExist:
				return HttpResponse('invalid user')
			except Article.DoesNotExist:
				return HttpResponse('invalid article')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def post_report_comment(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			author_id = request.POST['author_id']
			report_id = request.POST['report_id']
			content = request.POST['content']
			try:
				user = User.objects.get(id=author_id)
				report = Report.objects.get(id=report_id)
				comment = ReportComment(author=user, report=report, content=content)
				comment.tag = user.get_full_name()
				comment.save()
				return HttpResponse(str(comment.id))
			except User.DoesNotExist:
				return HttpResponse('invalid user')
			except Report.DoesNotExist:
				return HttpResponse('invalid report')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def post_article_like(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			author_id = request.POST['author_id']
			article_id = request.POST['article_id']
			try:
				user = User.objects.get(id=author_id)
				article = Article.objects.get(id=article_id)
				like = Like(user=user, article=article)
				like.save()
				return HttpResponse('liked')
			except User.DoesNotExist:
				return HttpResponse('invalid user')
			except Article.DoesNotExist:
				return HttpResponse('invalid article')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def post_article_unlike(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			author_id = request.POST['author_id']
			article_id = request.POST['article_id']
			try:
				Like.objects.filter(user__id=int(author_id), article__id=int(article_id)).delete()
				return HttpResponse('deleted')
			except Exception:
				return HttpResponse('invalid')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def post_report_like(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			author_id = request.POST['author_id']
			report_id = request.POST['report_id']
			try:
				user = User.objects.get(id=author_id)
				report = Report.objects.get(id=report_id)
				like = Like(user=user, report=report)
				like.save()
				return HttpResponse('liked')
			except User.DoesNotExist:
				return HttpResponse('invalid user')
			except Report.DoesNotExist:
				return HttpResponse('invalid report')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def post_report_unlike(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			author_id = request.POST['author_id']
			report_id = request.POST['report_id']
			try:
				Like.objects.filter(user__id=int(author_id), report__id=int(report_id)).delete()
				return HttpResponse('deleted')
			except Exception:
				return HttpResponse('invalid')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def view_article(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			article_id = request.POST['article_id']
			try:
				article = Article.objects.get(id=article_id)
				if article.view_count:
					article.view_count += 1
				else:
					article.view_count = 1
				article.save()
				return HttpResponse('viewed')
			except Article.DoesNotExist:
				return HttpResponse('invalid article')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def view_report(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			report_id = request.POST['report_id']
			try:
				report = Report.objects.get(id=report_id)
				if report.view_count:
					report.view_count += 1
				else:
					report.view_count = 1
				report.save()
				return HttpResponse('viewed')
			except Report.DoesNotExist:
				return HttpResponse('invalid report')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')

@csrf_exempt
def post_report(request):
	if request.method == 'POST':
		key = request.POST['key']
		if diff(key, REAL_SECRET_KEY) < 3:
			user_id = request.POST['author_id']
			report_title = request.POST['title']
			
			exists = Report.objects.filter(headline=report_title).count()
			if exists:
				return HttpResponse("exists")

			try:
				user = User.objects.get(id=int(user_id))

				report_content = request.POST.get('text', '')
				image = request.FILES.get('image', None)
				video = request.FILES.get('video', None)
				audio = request.FILES.get('audio', None)

				report = Report(author=user, headline=report_title)
				report.published = False
				report.content = report_content
				report.photo = image
				report.video = video
				report.audio = audio

				report.tag = user.get_full_name()

				report.save()
				return HttpResponse("saved")
			except User.DoesNotExist:
				return HttpResponse("invalid user")
			except Exception as error:
				# return HttpResponse(str(error))
				return HttpResponse('invalid report')
		else:
			return HttpResponse('invalid key')
	else:
		return HttpResponse('invalid request')