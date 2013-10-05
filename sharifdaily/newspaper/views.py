from django.http import HttpResponse
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from .models import *
from sharifdaily.accounts.views import REAL_SECRET_KEY
from sharifdaily.accounts.utils import diff

ARTICLES_PER_PAGE = 10
ARCHIVES_PER_PAGE = 10
REPORTS_PER_PAGE = 10
COMMENTS_PER_PAGE = 10

def get_articles(request, page):
	article_list = Article.objects.filter(published = True).values('id', 'date', 'headline', 'content', 'view_count', 'photo').order_by('-date')
	page = int(page)
	start = (page - 1) * ARTICLES_PER_PAGE
	end = page * ARTICLES_PER_PAGE
	return HttpResponse(simplejson.dumps(list(article_list[start:end]), cls=DjangoJSONEncoder))

def get_archives(request, page):
	archive_list = Archive.objects.values('date', 'title').order_by('-date')
	page = int(page)
	start = (page - 1) * ARCHIVES_PER_PAGE
	end = page * ARCHIVES_PER_PAGE
	return HttpResponse(simplejson.dumps(list(archive_list[start:end]), cls=DjangoJSONEncoder))

def get_reports(request, page):
	report_list = Report.objects.filter(published = True).values('date', 'headline', 'view_count', 'likes', 'content', 'photo', 'audio', 'video').order_by('-date')
	page = int(page)
	start = (page - 1) * REPORTS_PER_PAGE
	end = page * REPORTS_PER_PAGE
	return HttpResponse(simplejson.dumps(list(report_list[start:end]), cls=DjangoJSONEncoder))	

def get_article_comments(request, page, _id):
	try:
		article = Article.objects.get(id=int(_id))
		comment_list = ArticleComment.objects.filter(article=article, is_public=True).values('created', 'tag', 'content').order_by('-created')	
		page_num = int(page)
		start = (page_num - 1) * COMMENTS_PER_PAGE
		end = page_num * COMMENTS_PER_PAGE
		return HttpResponse(simplejson.dumps(list(comment_list[start:end]), cls=DjangoJSONEncoder))	
	except Article.DoesNotExist:
		return HttpResponse('invalid article')		

def get_report_comments(request, page, _id):
	try:
		report = Report.objects.get(id=int(_id))
		comment_list = ReportComment.objects.filter(report=report, is_public=True).values('created', 'tag', 'content').order_by('-created')	
		page_num = int(page)
		start = (page_num - 1) * COMMENTS_PER_PAGE
		end = page_num * COMMENTS_PER_PAGE
		return HttpResponse(simplejson.dumps(list(comment_list[start:end]), cls=DjangoJSONEncoder))	
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
				comment = reportComment(author=user, report=report, content=content)
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

# TODO: Post Report