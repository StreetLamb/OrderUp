import sys
import time
from pprint import pprint
import telepot
import os
from telepot.loop import MessageLoop
from datetime import datetime
from pytz import timezone
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup,ForceReply,KeyboardButton
from telepot.namedtuple import LabeledPrice, ShippingOption
from telepot.delegate import (
    per_invoice_payload, pave_event_space, create_open,
    per_message, call)

all_list=[]
orderee_list=[]
chat_list=[]
temp_dict={}
id_phonedict={}

robot=u'\U0001F916'
thumbsup=u'\U0001f44d'
sassy=u'\U0001f481'
cook=u'\U0001f373'
waiter=u'\U0001f935'
money=u'\U0001f4b0'
timer=u'\u231B'
pray=u'\U0001f64f'
phone=u"\U0001F4DE"
siren=u"\U0001F6A8"

def on_pre_checkout_query(msg):
    query_id, from_id, invoice_payload = telepot.glance(msg, flavor='pre_checkout_query')
    bot.answerPreCheckoutQuery(query_id, True)

def verify(chat_id):
    introMessage="Hi, OrderUp here! {}\nYou can use me to order food from Techno Edge! {} View a list of commands by typing '/'\nTo start, verify by sharing your phone number.".format(robot,thumbsup)
    markup=ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Verify phone number {}".format(phone),request_contact=True)]
        ])
    bot.sendMessage(chat_id,introMessage,reply_markup=markup)

##def on_chat_message2(msg):
##    content_type, chat_type, chat_id = telepot.glance(msg)
####    print(msg)
##    for i in chat_list:               
##        if i['user1']==str(chat_id):
##            if content_type=="text":
##                if msg['text']=="/bye":
##                    bot2.sendMessage(chat_id,"You are disconnected. Click here: /chat%s to reconnect."%i['user2'])
##                    chat_list.remove(i)
##                elif msg['text'].startswith("/chat"):
##                    break
##                    
##                else:
##                    bot2.sendMessage(int(i['user2']), "/chat{} says: ".format(chat_id))
##                    bot2.forwardMessage(int(i['user2']),chat_id,msg['message_id'])
##                    break
##    
##    if msg['text'].startswith("/chat"):
##        for i in chat_list:
##            if i['user1']==str(chat_id):
##                temp="/chat"+str(i['user2'])
##                chat_list.remove(i)
##                bot2.sendMessage(chat_id,"Previous chat was closed. Click here: %s to re-enter chat."%temp)
##        other_id=msg['text'][5:]
##        chat_pair={}
##        chat_pair['user1']=str(chat_id)
##        chat_pair['user2']=str(other_id)
##        chat_list.append(chat_pair)
##        bot2.sendMessage(chat_id,"You are connected to {}. Click here: /bye to close.".format(chat_pair['user2']))


def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
##    print(msg)

##    for i in chat_list:               
##            if i['user1']==str(chat_id):
##                if content_type=="text":
##                    if msg['text']=="/bye":
##                        bot2.sendMessage(chat_id,"You are disconnected. Click here: /chat%s to reconnect."%i['user2'])
##                        chat_list.remove(i)
##                        
##                    else:
##                        bot2.sendMessage(int(i['user2']), "/chat{} says: ".format(chat_id))
##                        bot2.forwardMessage(int(i['user2']),chat_id,msg['message_id'])
##                        break
                        
    if 'contact' in msg.keys():
            if msg['contact']['user_id']==chat_id:
                id_phonedict[chat_id]=msg['contact']['phone_number']
                bot.sendMessage(chat_id,"Verified! %s"%thumbsup)
                introMessage="You can choose to be an Orderer or an Orderee. An Orderer helps the Orderee to order food.\nWould like to be an Orderer or Orderee? %s"%sassy
                markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Orderer",callback_data="o1"),
                     InlineKeyboardButton(text="Orderee",callback_data="o2")]
                    ])
                bot.sendMessage(chat_id,introMessage,reply_markup=markup)
            else:
                bot.sendMessage(chat_id,"Eh who you trying to bluff?! Thats not your phone number!")
                verify(chat_id)
                
    elif 'successful_payment' in msg.keys():
            bot.sendMessage(chat_id, 'Wah you damn brudder. Thanks for the Kopi! Limpeh will remember you forever!!')
            bot.sendSticker(chat_id, 'CAADAgADJQADyIsGAAGoEDksgR1WpAI')

    elif content_type=="text":
        
        if msg['text']=="/start":
            verify(chat_id)

        elif msg['text'].startswith("/broadcast"):
            if chat_id==243431792:
                count=0 #count how many users in each batch to prevent spam
                for i in id_phonedict:
                    if count>=20:
                        time.sleep(1)
                        count=0
                    else:
                        count+=1
                    bot.sendMessage(i,msg)

        elif msg['text']=="/logs":
            if chat_id==243431792:
                print(id_phonedict)
                print(orderee_list)
                print(all_list)

        elif msg['text']=="/stop":
            for i in all_list:
                if i['userid']==str(chat_id):
                    all_list.remove(i)
            bot.sendMessage(chat_id,"Done! You won't receive anymore orders. However, you may still accept existing orders!")

        elif msg['text']=="/report":
            bot.sendMessage(chat_id,"If reporting user, let me know the user name, mobile number and the reason below.",reply_markup=ForceReply())
            
##        elif msg['text'].startswith("/chat"):
##            for i in chat_list:
##                if i['user1']==str(chat_id):
##                    temp="/chat"+str(i['user2'])
##                    chat_list.remove(i)
##                    bot2.sendMessage(chat_id,"Previous chat was closed. Click here: %s to re-enter chat."%temp)
##            other_id=msg['text'][5:]
##            chat_pair={}
##            chat_pair['user1']=str(chat_id)
##            chat_pair['user2']=str(other_id)
##            chat_list.append(chat_pair)
##            bot2.sendMessage(chat_id,"You are connected to {}. Click here: /bye to close.".format(chat_pair['user2']))
##            bot.sendMessage(chat_id, "You are connected. Click here to chat: @orderup_chatbot")
            

        elif msg['text']=="/status":
            o1_stall_1=0
            o1_stall_2=0
            o1_stall_3=0
            o1_stall_4=0
            o1_stall_5=0
            o1_stall_6=0
            o1_stall_7=0
            o1_stall_8=0
            o1_stall_9=0
            o1_stall_10=0
            o1_stall_11=0
            o1_stall_12=0
            o1_stall_13=0
            o1_stall_14=0
##            o2_stall_1=0
##            o2_stall_2=0
##            o2_stall_3=0
##            o2_stall_4=0
##            o2_stall_5=0
##            o2_stall_6=0
##            o2_stall_7=0
##            o2_stall_8=0
##            o2_stall_9=0
##            o2_stall_10=0
##            o2_stall_11=0
##            o2_stall_12=0
##            o2_stall_13=0
##            o2_stall_14=0
            for i in all_list:
                if i["stall"]=="1":
                    o1_stall_1+=1
                elif i["stall"]=="2":
                    o1_stall_2+=1
                elif i["stall"]=="3":
                    o1_stall_3+=1
                elif i["stall"]=="4":
                    o1_stall_4+=1
                elif i["stall"]=="5":
                    o1_stall_5+=1
                elif i["stall"]=="6":
                    o1_stall_6+=1
                elif i["stall"]=="7":
                    o1_stall_7+=1
                elif i["stall"]=="8":
                    o1_stall_8+=1
                elif i["stall"]=="9":
                    o1_stall_9+=1
                elif i["stall"]=="a":
                    o1_stall_10+=1
                elif i["stall"]=="b":
                    o1_stall_11+=1
                elif i["stall"]=="c":
                    o1_stall_12+=1
                elif i["stall"]=="d":
                    o1_stall_13+=1
                elif i["stall"]=="e":
                    o1_stall_14+=1
                    
##            for j in orderee_list:
##                if j["options"][1]=="1":
##                    o2_stall_1+=1
##                elif j["options"][1]=="2":
##                    o2_stall_2+=1
##                elif j["options"][1]=="3":
##                    o2_stall_3+=1
##                elif j["options"][1]=="4":
##                    o2_stall_4+=1
##                elif j["options"][1]=="5":
##                    o2_stall_5+=1
##                elif j["options"][1]=="6":
##                    o2_stall_6+=1
##                elif j["options"][1]=="7":
##                    o2_stall_7+=1
##                elif j["options"][1]=="8":
##                    o2_stall_8+=1
##                elif j["options"][1]=="9":
##                    o2_stall_9+=1
##                elif j["options"][1]=="a":
##                    o2_stall_10+=1
##                elif j["options"][1]=="b":
##                    o2_stall_11+=1
##                elif j["options"][1]=="c":
##                    o2_stall_12+=1
##                elif j["options"][1]=="d":
##                    o2_stall_13+=1
##                elif j["options"][1]=="e":
##                    o2_stall_14+=1
                    
            message=("*Soya Milk*\nOrderer: {}\n*Fruit Juice*\nOrderer: {}\n*Chinese Food*\nOrderer: {}\n"
            "*Western Food*\nOrderer: {}\n*Chicken Rice*\nOrderer: {}\n*Japanese Food*\nOrderer: {}\n"
                     "*Ramen Corner*\nOrderer: {}\n*Yong Tau Foo*\nOrderer: {}\n*Vegetarian Food*\nOrderer: {}\n"
                     "*Fishball Noddles*\nOrderer: {}\n*Indian Food*\nOrderer: {}\n*Indonesian Food*\nOrderer: {}\n"
                     "*Drinks and Snacks*\nOrderer: {}\n*McDonalds*\nOrderer: {}\n".format(
                o1_stall_1,
                o1_stall_2,
                o1_stall_3,
                o1_stall_4,
                o1_stall_5,
                o1_stall_6,
                o1_stall_7,
                o1_stall_8,
                o1_stall_9,
                o1_stall_10,
                o1_stall_11,
                o1_stall_12,
                o1_stall_13,
                o1_stall_14))
            bot.sendMessage(chat_id,message,parse_mode="Markdown")

        elif msg['text']=="/orders":
            my_orderer_msg="---My orders for today---\n" #showing who your orderers
            my_orderee_msg="---What I'm ordering for others today---\n" #showing who you ordering for
            temp_num=0
            for i in all_list:
                if str(chat_id) in i['orderees']:
                    for k in orderee_list:
                        if 'orderer' in k.keys() and str(k['orderer'])==i['userid']:
                            temp_num+=1
                            my_orderer_msg+="{}) Orderer id: {}\nStall: {}\nOrder: {}\nTip: {}\n[CLICK HERE TO CHAT](tg://user?id={})\n\n".format(temp_num,i['userid'],i['stall'],k['order'],k['tip'],i['userid'])
                            
            bot.sendMessage(chat_id,my_orderer_msg,parse_mode="Markdown")
            temp_num=0
            for j in orderee_list:
                if 'orderer' in j.keys() and j['orderer']==chat_id:
                    temp_num+=1
                    my_orderee_msg+="{}) Orderee id: {}\nStall: {}\nOrder: {}\nTip: {}\n[CLICK HERE TO CHAT](tg://user?id={})\n\n".format(temp_num,j['userid'],j['options'][1],j['order'],j['tip'],j['userid'])
            bot.sendMessage(chat_id,my_orderee_msg,parse_mode="Markdown")


        elif 'reply_to_message' in msg.keys():
            if "Type your orders clearly below!" in msg['reply_to_message']['text']:
                if chat_id in temp_dict.keys():
                    orderee_info_dict=temp_dict[chat_id]
                    orderee_info_dict['order']=msg['text']
                    temp_dict[chat_id]=orderee_info_dict
                        
##                for i in orderee_list:
##                    if str(chat_id) in i['userid'] and "order" not in i.keys():
##                        i['order']=msg['text']
##                        break
                
                bot.sendMessage(chat_id,"Type your tip amount! Pay your Orderer when you collect your food!",reply_markup=ForceReply())

            elif "Type your tip amount! Pay your Orderer when you collect your food!" in msg['reply_to_message']['text']:
                if chat_id in temp_dict.keys():
                    orderee_info_dict=temp_dict[chat_id]
                    orderee_info_dict['tip']=msg['text']
                    temp_dict[chat_id]=orderee_info_dict
                bot.sendMessage(chat_id, "Type a location to meet!",reply_markup=ForceReply())

            elif "Type a location to meet!" in msg['reply_to_message']['text']:
                orderer_num_int=0
                if chat_id in temp_dict.keys():
                    orderee_info_dict=temp_dict[chat_id]
                    orderee_info_dict['location']=msg['text']
                    temp_options=orderee_info_dict['options']
                    temp_order=orderee_info_dict['order']
                    temp_tip=orderee_info_dict['tip']
                    temp_location=orderee_info_dict['location']
                
##                for i in orderee_list:
##                    if str(chat_id)in i['userid'] and "tip" not in i.keys():
##                        i['tip']=msg['text']
##                        temp_options=i['options']
##                        temp_order=i['order']
##                        temp_tip=i['tip']
##                        break
                    
                markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Accept",callback_data="A"+temp_options+str(chat_id))]
                                             ])

                markup1=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Cancel",callback_data="C"+temp_options+str(chat_id))]
                                             ])
                
                for j in all_list:
                    if j['stall']==temp_options[1]:
                        orderer_num_int+=1
                        bot.sendMessage(j["userid"],"Found an Orderee!\nOrder: {}\nTip: {}\nMeet: {}\nTo stop receiving: /stop".format(temp_order,temp_tip,temp_location),reply_markup=markup)

                message_with_inline_keyboard=None
                message_with_inline_keyboard=bot.sendMessage(chat_id, "{} orderers in the queue so far. Waiting for Orderers... {}".format(orderer_num_int,timer) ,reply_markup=markup1)
                orderee_info_dict['kmsg']=message_with_inline_keyboard
                orderee_list.append(orderee_info_dict)
                del temp_dict[chat_id]

            elif "If reporting user, let me know the user name, mobile number and the reason below." in msg['reply_to_message']['text']:
                bot.forwardMessage(243431792,chat_id,msg['message_id'])

                
        elif msg['text']=="/donate":
            bot.sendInvoice(chat_id,
                            "Donation", "Buy me Kopi if you like this project and would like to see it improve!",
                            payload='a-string-identifying-related-payment-messages-tuvwxyz',
                            provider_token='350862534:LIVE:ODg0ZDRiYzU3ZmY1',
                            start_parameter='abc',
                            currency='SGD', prices=[
                                LabeledPrice(label='Kopi', amount=300)],photo_url='https://goo.gl/4Mv7he',photo_size=4096,photo_width=64,photo_height=64)
            

                    
        
            
def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
##    print('Callback Query:', query_id, from_id, query_data)
    if query_data=="o1" or query_data=="o2":

        keyboard=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="Soya Milk", callback_data="s1"+query_data),
                     InlineKeyboardButton(text="Fruit Juice", callback_data="s2"+query_data)],
                    
                    [InlineKeyboardButton(text="Chinese Food", callback_data="s3"+query_data),
                     InlineKeyboardButton(text="Western", callback_data="s4"+query_data)],

                    [InlineKeyboardButton(text="Chicken Rice", callback_data="s5"+query_data),
                     InlineKeyboardButton(text="Japanese", callback_data="s6"+query_data)],

                    [InlineKeyboardButton(text="Ramen Corner", callback_data="s7"+query_data),
                     InlineKeyboardButton(text="Yong Tau Foo", callback_data="s8"+query_data)],

                    [InlineKeyboardButton(text="Vegetarian", callback_data="s9"+query_data),
                     InlineKeyboardButton(text="Fishball Noodles", callback_data="sa"+query_data)],

                    [InlineKeyboardButton(text="Indian Food", callback_data="sb"+query_data),
                     InlineKeyboardButton(text="Indonesian Food", callback_data="sc"+query_data)],
                    
                    [InlineKeyboardButton(text="Drinks and Snacks", callback_data="sd"+query_data),
                     InlineKeyboardButton(text="McDonald's", callback_data="se"+query_data)]
                    ]
                )
        if query_data=="o1":
            user_type_text="Orderer"
            message="Hi fellow %s! %s Please select the stall you are queuing for! %s"%(user_type_text,waiter,cook)
        else:
            user_type_text="Orderee"
            message="Hi fellow %s! Please select a stall! %s"%(user_type_text,cook)
        
        bot.sendMessage(from_id, message, reply_markup=keyboard)

    elif query_data[0]=="s" and query_data[3]=="2" and len(query_data)==4:
        orderee_info_dict={}
        orderee_info_dict['userid']=str(from_id)
        orderee_info_dict['options']=query_data
        orderee_info_dict['accepted']=0
        try:
            orderee_info_dict['phone_number']=id_phonedict[from_id]
        except:
            bot.sendMessage(from_id,"Sorry we need you to verify again! {}".format(pray))
            verify(from_id)
        else:
##        orderee_list.append(orderee_info_dict)
            temp_dict[from_id]=(orderee_info_dict)
            bot.sendMessage(from_id, "Type your orders clearly below!",reply_markup=ForceReply())
        

    elif query_data[0]=="s" and query_data[3]=="1":
        valid_queuer=True
        for i in all_list:
            if i['userid']==str(from_id) and i['stall']==str(query_data[1]):
                valid_queuer=False
                bot.sendMessage(from_id,"You are already an Orderer for this stall!")
                
        if valid_queuer==True:
            
            message_with_inline_keyboard=None
            orderer_info_dict={}
            orderer_info_dict['userid']=str(from_id)
            orderer_info_dict['stall']=query_data[1]
            try:
                orderer_info_dict['phone_number']=id_phonedict[from_id]
            except:
                bot.sendMessage(from_id, "Sorry we need you to verify again! {}".format(pray))
                verify(from_id)
            else:
                orderer_info_dict['orderees']=[]
                markup=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Cancel",callback_data="Z"+orderer_info_dict['stall'])]
                                                 ])
                message_with_inline_keyboard=bot.sendMessage(from_id, "You are now an Orderer! %s Be patient while we connect you with Orderees!"%waiter,reply_markup=markup)
                orderer_info_dict['kmsg']=message_with_inline_keyboard
                all_list.append(orderer_info_dict)
                

                for i in orderee_list:
                    if i["options"][1]==query_data[1]:
                        temp_options=i['options']
                        temp_order=i['order']
                        temp_tip=i['tip']
                        temp_location=i['location']
                        markup1=InlineKeyboardMarkup(inline_keyboard=[
                        [InlineKeyboardButton(text="Accept",callback_data="A"+temp_options+str(from_id))]
                                                 ])
                        bot.sendMessage(from_id,"Found an Orderee!\nOrder: {}\nTip: {}\nMeet: {}\nTo stop receiving: /stop".format(temp_order,temp_tip,temp_location),reply_markup=markup1)

    elif query_data[0]=="A":
        found_orderee=False
        for i in orderee_list:
            if i['userid']==query_data[5:] and i['options']==query_data[1:5] and i['accepted']==0:
                i['accepted']=1
                temp=query_data[5:]
                i['orderer']=from_id
                found_orderee=True
                msg_idf=telepot.message_identifier(i['kmsg'])
                bot.editMessageReplyMarkup(msg_idf)
                break
            
        if found_orderee==True:
            for j in all_list:
                if j['userid']==str(from_id) and j['stall']==str(query_data[2]):
                    j['orderees'].append(temp)
                    msg_idf=telepot.message_identifier(j['kmsg'])
                    bot.editMessageReplyMarkup(msg_idf)
                    break
            
            bot.sendMessage(from_id,"Nice one la! {} See your orders here: /orders To chat with your Orderee, [CLICK HERE](tg://user?id={})".format(thumbsup,query_data[5:]),parse_mode="Markdown")
            bot.sendMessage(query_data[5:],"Wah swee la! {} Your order has been accepted! See your orders here: /orders To chat with your Orderer, [CLICK HERE](tg://user?id={})".format(thumbsup,from_id), parse_mode="Markdown")
            
        else:
            bot.sendMessage(from_id,"Someone already accepted the order!")


    elif query_data[0]=="C":
        
        for i in orderee_list:
            if i["userid"]==str(from_id) and i["options"]==str(query_data[1:5]):
                orderee_list.remove(i)
                bot.sendMessage(from_id,"Order cancelled!")

    elif query_data[0]=="Z":
        for i in all_list:
            if i["userid"]==str(from_id) and i["stall"]==query_data[1]:
                all_list.remove(i)
                bot.sendMessage(from_id,"Cancelled!")
                break




TOKEN1=##Add you token here

bot=telepot.Bot(TOKEN1)
MessageLoop(bot,{'chat': on_chat_message,'callback_query': on_callback_query, 'pre_checkout_query': on_pre_checkout_query}).run_as_thread()
day=0

while 1:
    singapore = timezone('Asia/Singapore')
    global sg_time
    sg_time = datetime.now(singapore)
    if sg_time.strftime('%d')!=day:
        day=sg_time.strftime('%d')
        all_list=[]
        orderee_list=[]
    time.sleep(10)
    




