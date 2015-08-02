from django import forms

class BlogForm(forms.Form):
	title=forms.CharField(label="your title",
				required=True,
				error_messages={'required':'please code your valid title'},
				widget=forms.TextInput(attrs={"class":'form-control',"placeholder":"write your titlehere"}))
	body=forms.CharField(label="body",
					required=True,
					error_messages={'required':'body is needed'},
					widget=forms.Textarea(attrs={"class":'form-control',"placeholder":"write your passage here",})
				)
	summury=forms.CharField(label="summury",
					required=True,
					error_messages={'required':'summury is needed'},
					widget=forms.Textarea(attrs={"class":'form-control',"placeholder":"write your summury here","style":"height:200px;"})
				)


	def cleaned_body(self):
		body=self.cleaned_data['body']
		lgt=len(body)
		if lgt<15:
			raise forms.ValidationError("body must be more than 15 characters")
		return body

class CommentForm(forms.Form):
	comment=forms.CharField(label="comment",
					required=True,
					error_messages={'required':'comment is needed'},
					widget=forms.Textarea(attrs={"class":'form-control',"placeholder":"write your comment here","style":"height:150px;"})
				)


	def cleaned_comment(self):
		body=self.cleaned_data['comment']
		lgt=len(body)
		if lgt<5:
			raise forms.ValidationError("body must be more than 5 characters")
		return body
