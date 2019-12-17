from flask import Flask, request, session
from twilio.twiml.messaging_response import MessagingResponse
from py_edamam import PyEdamam
import time
import atexit
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

# The session object makes use of a secret key.
SECRET_KEY = '###############################'
app = Flask(__name__)
app.config.from_object(__name__)

def edamam(food):

	e = PyEdamam(recipes_appid='#######', recipes_appkey='###########')

	for recipe in e.search_recipe(food):
		return recipe,recipe.url

def run(dictionary):
	mini = 1000000000
	#Before, you were printing that everything in your dictionary was expiring and a recipe for everything
	#Now, we are looking ONLY for the thing with minimum days left and only printing a recipe for that.
	message=""
	for each in dictionary:
    		if int(dictionary[each]) < int(mini):
    			if int(dictionary[each]) == 0:
    				message = message + "Oh no! Your " + str(each) + " expires today!\n"
    				del dictionary[each]
    			mini = dictionary[each] #This is how many days left of minimum item
    			food = each #and this is the item name
    	#dictionary[each]=str(int(dictionary[each])-1)

	recipe, recipe_url = edamam(food)
	message =str("Your " + str(food) + " is expiring in " + str(mini) + " days! Why not try this recipe for " + str(recipe) + "? \n" + str(recipe_url))
	print(message)
	return message


@app.route("/", methods=['GET', 'POST'])
def hello():
    """Respond with the number of text messages sent between two parties."""
    # Increment the counter
    counter = session.get('counter', 0)
    dictionary = session.get('dictionary', {})
    grocery = session.get('grocery', "")
    expiry = session.get('expiry', "")
    message = ""
    if request.form['Body'] == "No":
    	counter = 4
    	# get smallest value and it's key and print
    	mini = 1000000000

    	for each in dictionary:
    		if int(dictionary[each]) < int(mini):
    			mini = dictionary[each]
    			food = each
    	message = "Ok, just so you know, " + str(food) + " is expiring in " + str(mini) + " days! Text Recipe if you need recipe suggestions!"
    elif counter>2:
    	counter = 0
    	
    counter += 1

    # Save the new counter value in the session

    from_number = request.values.get('From')

    # Build our reply
    if request.form['Body'] == 'Recipe' or request.form['Body'] == 'Recipe ':
    	message = run(dictionary)
    	counter = 0
    elif counter == 1:
    	message = 'What did you buy?' 
    elif counter == 2:
    	message = 'Sounds delicious! How many days will it take to expire?'
    	grocery = request.form['Body']
    elif counter == 3:
    	message = 'Sounds great! We will let you know when its expired! Would you like to enter another food? (Yes/No?)'
    	expiry = request.form['Body']
    	dictionary[grocery] = expiry
    # Put it in a TwiML response
    session['dictionary'] = dictionary
    session['grocery'] = grocery
    session['counter'] = counter
    time = datetime.datetime.now()
    hour = time.hour


    resp = MessagingResponse()
    resp.message(message)

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
