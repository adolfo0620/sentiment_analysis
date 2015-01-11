from django.shortcuts import render
from django.views.generic import View
from sa_api.api import Score

# Create your views here.

class Index( View ):
	def get( self, request ):
		return render( request, 'testMod/index.html', request.context_dict )

class Block( View ):
	def post( self, request ):
		score = Score()
		score.eval( request.POST.get( 'text', '' ) )
		request.context_dict['score'] = score
		request.context_dict['text'] = request.POST.get( 'text', '' )

		return render( request, 'testMod/results.html', request.context_dict)
