# -*- coding: utf-8 -*-
"""
Created on Mon Sep 09 13:59:07 2013

@author: Joachim.BARBAY


TODO : see http://www.trirand.com/jqgridwiki/doku.php?id=wiki:adjacency_model

_field			number	this field determines the level in the hierarchy of the element. Usually the root element will be at level 0.The first child of the root is at level 1 and so on. This information is needed for the grid to set the ident of every element.
parent_id_field	mixed		indicates if the record has a parent with an id of parent_id_field. If the parent id is NULL the element is a root element
leaf_field		boolean	This field should tell the grid that the element is leaf. Possible values can be true and false. To the leaf element is attached diffrent image and this element can not be expanded or collapsed.
expanded_field	boolean	Tells the grid whether this element should be expanded during the loading (true or false). If the element has no value, false is set. Note that the data can be empty for this element, but this element can not be removed from data set.


	echo "<row>";         
      echo "<cell>". $row[account_id]."</cell>";
      echo "<cell>". $row[name]."</cell>";
      echo "<cell>". $row[acc_num]."</cell>";
      echo "<cell>". $row[debit]."</cell>";
      echo "<cell>". $row[credit]."</cell>";
      echo "<cell>". $row[balance]."</cell>";
      
      
      echo "<cell>". $level."</cell>";
      if(!$row[parent_id]) $valp = 'NULL'; else $valp = $row[parent_id];  // parent field
      echo "<cell><![CDATA[".$valp."]]></cell>";
      if($row[account_id] == $leafnodes[$row[account_id]]) $leaf='true'; else $leaf = 'false';  // isLeaf comparation
      echo "<cell>".$leaf."</cell>"; // isLeaf field
      echo "<cell>false</cell>"; // expanded field
      echo "</row>";
      
      
      <script>
...
jQuery("#treegrid").jqGrid({
    treeGrid: true,
    treeGridModel: 'adjacency',
    ExpandColumn : 'name',
    url: 'server.php?q=tree',
    datatype: "xml",
    mtype: "POST",
    colNames:["id","Account","Acc Num", "Debit", "Credit","Balance"],
    colModel:[
         {name:'id',index:'id', width:1,hidden:true,key:true},
         {name:'name',index:'name', width:180},
         {name:'num',index:'acc_num', width:80, align:"center"},
         {name:'debit',index:'debit', width:80, align:"right"},      
         {name:'credit',index:'credit', width:80,align:"right"},      
         {name:'balance',index:'balance', width:80,align:"right"}      
    ],
    height:'auto',
    pager : "#ptreegrid",
    caption: "Treegrid example"
});
...
</script>
"""

from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
app = Flask(__name__)

includes="""js/kinetic-v4.6.0.min.js
            js/i18n/grid.locale-en.js
            jquery.layout-latest.js
            js/jquery.jqGrid.min.js
            css/ui.jqgrid.css
            css/layout-default-latest.css
            themes/ui.multiselect.css"""

@app.route("/")
def hello():
	#print url_for("static", filename="style.css")
	return  render_template("jqlayout.html")
	#return  render_template("hello.html",msg=url_for("static", filename="jqgrid_demo40/jqgrid.html"))

#os.system(r"C:\Users\joachim.barbay\AppData\Local\Google\Chrome\Application\chrome.exe --disable-web-security")

@app.route("/coucou")
def coucou():
	#print url_for("static", filename="style.css")
	return "coucou2"

@app.route("/test")
def show_entries():
	#cur = g.db.execute(’select title, text from entries order by id desc’)
	#entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
	return render_template("show_entries.html", entries=entries)

if __name__ == "__main__":
	import webbrowser
	webbrowser.open('http://127.0.0.1:5000')
	#webbrowser.open('http://127.0.0.1:5000/static/jqgrid_demo40/jqgrid.html')
	#webbrowser.open('http://127.0.0.1:5000/static/jqgrid_demo40/jqgrid.html')
	app.run(debug=True)
    

class JqGridColumn():
    """http://www.trirand.com/jqgridwiki/doku.php?id=wiki:colmodel_options
    datefmt
    
    editrules :{name:'price', ..., editrules:{edithidden:true, required:true number:true}, editable:true },
    edittype : text | textarea | checkbox | select | password | file
    editoptions : 
    http://www.trirand.com/jqgridwiki/doku.php?id=wiki:common_rules#editable
    """
    def __init__(self,name,index="",width=90,label=None,editable=True,sortable=False,resizable=True,key=False,hidden=False,align="left",title=False,edittype=None,editoptions="",**kargs):
        self.name=name
        self.index=index
        self.label=label or name
        
        self.width=width
        self.editable=editable
        self.sortable=sortable
        self.resizable=resizable
        self.hidden=hidden
        self.key=key
        
        self.align=align
        self.title=title
        self.edittype=edittype
        self.editoptions=editoptions
        self.module_key=False
        self.module_Field=False
        
        self.__dict__.update(kargs)

    def toJavaString(self):  
        javaString="name:'{name}', index:'{index}', width:{width}".format(**self.__dict__)
        if self.label : javaString+= ', label:"%s"'%self.label  
        javaString+= ", sortable:true" if self.sortable else ", sortable:false"
        javaString+= ", editable:true" if self.editable else ", editable:false"
        javaString+= ", resizable:true" if self.resizable else ", resizable:false"
        if self.key : javaString+= ", key:true"  
        if self.title : javaString+= ", title:true"  
        if self.hidden : javaString+= ", hidden:true"  
        if self.edittype : javaString+= ', edittype:"%s"'%self.edittype    
        if self.editoptions : javaString+= ', editoptions:%s'%self.editoptions    
        return "{ "+javaString +"}"

from collections import namedtuple
#move to catalogue def
#      
class JqGridTableDef(list):
    def __init__(self,*args):
        super(JqGridTableDef,self).__init__(args)
        self.RowClass=namedtuple("rowRecord",[jqGridColumn.name for jqGridColumn in self])
    @property
    def colModel(self):
        return "["+",\n".join(map(JqGridColumn.toJavaString,self))  + "]" 
    
    @property
    def colNames(self):
        return repr([d.label for d in headers])
    
    @property
    def moduleFields(self):
        return [col.toJavaString() for col in self if (col.module_key or col.module_Field) ]
    @property
    def moduleFieldsNames(self):
        return [col.name for col in self if (col.module_key or col.module_Field) ]
    @property
    def moduleModel(self):
        return "[" + ",\n".join(self.moduleFields )  + "]" 
    
    def getDataModule(self,module):
        return [ getattr(module,fieldName) for fieldName in self.moduleFieldsNames]
        
    def addMaterial(self,module,row):
        pass
        #modules[moduleKey].addMaterial(rep,description,quantity,moduleRef)    
        

 
headers=JqGridTableDef(
        JqGridColumn("name",sortable=True),
        JqGridColumn("index",sortable=True),
        JqGridColumn("label",editable=False,resizable=True),
        JqGridColumn("width"),
        JqGridColumn("sortable",width=30,edittype="checkbox",editoptions="""{'value':"Oui:Non"}"""),
        JqGridColumn("editable",width=30,edittype="checkbox",editoptions="""{'value':"Oui:Non"}"""),
        JqGridColumn("resizable",width=30,edittype="checkbox",editoptions="""{'value':"Oui:Non"}""",hidden=True),
        JqGridColumn("module_key",width=30,edittype="checkbox",editoptions="""{'value':"Oui:Non"}"""),
        JqGridColumn("module_Field",width=30,edittype="checkbox",editoptions="""{'value':"Oui:Non"}"""),
        )
#ne supporte pas l'unicode !!
headers=JqGridTableDef(
        JqGridColumn("rep",label="repere",sortable=True),
        JqGridColumn("description",sortable=True),
        JqGridColumn("quantity",sortable=True),
        JqGridColumn("moduleRef",sortable=True,module_key=True),
        JqGridColumn("moduleDesc",sortable=True,module_Field=True),
        JqGridColumn("refCommande",sortable=True,module_Field=True),
        
       
        )