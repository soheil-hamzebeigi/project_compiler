from antlr4 import *
# pip install antlr4-python3-runtime
# import understand as und
from gen.JavaLexer import JavaLexer
from gen.JavaParserLabeled import JavaParserLabeled
from gen.JavaParserLabeledListener import JavaParserLabeledListener
import os
from os import path

class Mylistener(JavaParserLabeledListener):
    def __init__(self):
        self.field_list = []
        self.field_list_2 = []

    def entermethodDecleration(self, ctx: JavaParserLabeled.CompilationUnitContext):
        self.field_list.append(ctx.formalParameters().getText)
        self.field_list_2.append(ctx.qualifiedNameList().getText)


def main():
    try:
        import understand as und
        from openunderstand.db.api import create_db
        from openunderstand.db.fill import main
        from openunderstand.db.models import ModelName, EntityModel, ReferenceModel, KindModel
        # from db.models import EntityModel, ReferenceModel
    except ImportError:
        print("Can not import understand")

    db = und.open("F:\Antlr\project\OpenUnderstand-master\OpenUnderstand-master.udb")

    ref_array = []
    type_array = []
    simple = []
    line = []
    column = []
    val = []
    cont = []
    ids = []
    kind = []
    for ent in db.ents():
        for ref in ent.refs():
            if ref == "throw":
                ref_array.append(ref.id())
                type_array.append(ref.ent.type())
                simple.append(ref.ent.simplename())
                line.append(ref.ent.line())
                column.append(ref.ent.column())
                val.append(ref.ent.value())
                cont.append(ref.ent.contents())
                ids.append(ref.ent.id())
                kind.append(ref.ent.kind())

    paths = "F:\Antlr\session 4\compiler1400"

    filelist = []

    for root, dirs, files in os.walk(paths):
        # print(dirs)
        for filee in files:
            # print(file)
            if ".java" in filee:
                # filehandle = open(file, 'r')
                # print(filee)
                # print(os.path.join(root, filee))
                # open both files
                x = os.path.join(root, filee)
                # print(x)
                f = open(x, "r")
                for c in f:
                    # print(c)
                    f = open("F:\Antlr\project\project.txt", "a")
                    f.write(c)
                    f.close()

    try:
        input_steam = FileStream("F:\Antlr\project\project.txt")
        lexer = JavaLexer(input_steam)
        tokens = CommonTokenStream(lexer)
        parser = JavaParserLabeled(tokens)
        tree = parser.compilationUnit()
        listener = Mylistener()
        walker = ParseTreeWalker()

        walker.walk(
            listener=listener,
            t=tree
        )
    except:
        print("")

    create_db(
        dbname="F:\Antlr\project\OpenUnderstand-master\openunderstand\analysis_passes\database.db",
        # customize the path
        project_dir="F:\Antlr\project\OpenUnderstand-master\openunderstand\analysis_passes"  # customize the path
    )

    java_package_kind = KindModel.get_or_none(is_ent_kind=True, _name="throw")
    for i in range(listener.field_list[0]):
        EntityModel.get_or_create(_id=ids[i], _type=type_array[i], _kind=kind[i], _value=val[0],
                                  _parent=listener.field_list[i], _name=simple[i],
                                  _longname="{}.{}".format(listener.field_list[i],simple[i]),
                                  _contents=cont[i])
        ReferenceModel.get_or_create(_line=line[i], _column=column[i])


if __name__ == '__main__':
     main()

