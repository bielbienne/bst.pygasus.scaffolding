from zope import schema

from bb.extjs.core import ext
from bb.extjs.scaffolding.fields import BuilderBase
from bb.extjs.scaffolding.interfaces import IScaffoldingRecipeForm


class BuilderBaseForm(BuilderBase):
    ext.baseclass()

    def default(self):
        return dict(name=self.field.getName(),
                    fieldLabel=self.field.title,
                    emptyText=self.field.default,
                    allowBlank=self.field.required
                    )
        

class StringField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IField)
    def __call__(self):
        di = self.default()
        di.update(dict(xtype='textfield'))
        if self.field.max_length is not None:
            di['maxLength']=self.field.max_length
        if self.field.min_length is not None:
            di['minLength']=self.field.min_length
        return di


class PasswordField(StringField):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IPassword)
    def __call__(self):
        di = super(PasswordField, self).__call__()
        di.update(dict(inputType='password'))
        return di


class DateField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IDate)
    def __call__(self):
        di = self.default()
        di.update(dict(xtype='datefield'))
        return di


class CheckboxField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IBool)
    def __call__(self):
        di = self.default()
        di.update(dict(xtype='checkboxfield'))
        return di


class IntField(BuilderBaseForm):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IInt)
    def __call__(self):
        di = self.default()
        di.update(dict(xtype='numberfield'))
        return di


class IdField(IntField):
    ext.adapts(IScaffoldingRecipeForm, schema.interfaces.IId)
