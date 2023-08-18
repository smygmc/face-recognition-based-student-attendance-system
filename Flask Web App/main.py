from website import create_app


app=create_app()

if __name__=='__main__':
    app.run(debug=True) # debug true means kod her değiştiğinde tekrar kendisi re run etsin productionda bunu kaldırmak gerek sadece sen istediğinde rerun etmek için
