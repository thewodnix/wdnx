from flask import Flask, render_template

app = Flask(__name__)


@app.route('/table/<gender>/<age>')
def table(gender, age):
    age = int(age)
    if gender == 'male':
        if age < 21:
            wall_color = 'lightblue'
        else:
            wall_color = 'blue'
    else:
        if age < 21:
            wall_color = 'pink'
        else:
            wall_color = '#661e76'

    if age < 21:
        alien_image = '/static/img_1.png'
    else:
        alien_image = '/static/img.png'

    return render_template('distribution.html', wall_color=wall_color, alien_image=alien_image)



if __name__ == '__main__':
    app.run(debug=True)