from wtforms.validators import ValidationError

class Unique(object):

    def __init__(self, model, field, message=None):
        self.model = model
        self.field = field
        if not message:
            message = u'this element already exists'
        self.message = message

    def __call__(self, form, field):         
        check = self.model.query.filter(self.field == field.data).first()
        if check:
            raise ValidationError(self.message)

        query = self.query
        query = query.filter(getattr(self.model,field.id)== form[field.id].data)
        if form[self.pk].data:
            query = query.filter(getattr(self.model,self.pk)!=form[self.pk].data)
        obj = query.first()
        if obj:
            if self.message is None:
                self.message = field.gettext(u'Already exists.')
            raise ValidationError(self.message)