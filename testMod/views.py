from django.shortcuts import render
from django.views.generic import View
from sa_api.api import Score
from Query.models import Query
from django.contrib.auth.models import User

class Index( View ):
	def get( self, request ):
		return render( request, 'testMod/index.html', request.context_dict )

class Block( View ):
	def post( self, request ):
		text = request.POST.get( 'text', '' )

		score = Score()
		score.eval( text )
		request.context_dict['score'] = score
		request.context_dict['text'] = request.POST.get( 'text', '' )

		Query.objects.create(query_string = text,
							negative_score = score.neg,
							positive_score = score.pos,
							user=request.user,
							media_platform="textmod"
							)

		return render( request, 'testMod/results.html', request.context_dict)
