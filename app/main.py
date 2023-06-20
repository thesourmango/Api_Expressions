import os
from flask import Flask, jsonify,request
from dotenv import load_dotenv
from flask_cors import CORS

# Load variables from .env
load_dotenv()
print(os.environ.get('HELLO'))

# Create Flask instance
app = Flask(__name__)

#Allowing acess for our localhost only 
CORS(app, resources={r'/*':{'origins':'http://127.0.0.1:5500'}})

#Allows UTF-8 in JSON
app.config['JSON_AS_ASCII']=False


#Test data
face_data=[
    {
        'id':0,
        'name':"smile",
        'mouth':"m 97.3423,213.19999 c 8.4419,6.97268 18.84406,16.35992 28.37838,20.03725 3.58744,1.33113 17.55481,6.18499 21.34908,6.12313 4.22117,0.0132 19.81861,-5.38315 21.89891,-6.42613 11.61071,-4.43883 20.13472,-11.22679 29.13472,-19.46698 -11.78149,8.72469 -11.86217,9.78333 -25.06561,16.51813 -4.33334,2.21034 -22.59321,7.84542 -25.97284,8.04015 -2.96885,-0.11472 -17.77123,-4.37283 -24.46975,-7.51833 -9.76665,-4.58625 -13.51862,-9.44092 -25.25289,-17.30722 z",
        'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,-24.37947 16.819944,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z",
    },
    {
        'id':1,
        'name':"neutral",
        'mouth': "m 94.938837,213.06828 c 11.182233,-0.21635 12.957763,-0.39527 23.742453,0.0919 8.66395,0.60599 17.0513,0.82029 23.91524,1.67053 9.13486,0.55376 14.88731,0.98009 24.71612,1.64509 13.90796,2.01439 20.38005,0.11545 31.9476,1.50621 -11.51422,0.47088 -8.93666,0.91308 -15.63422,1.00931 -5.29019,0.076 -37.6628,-2.40964 -41.04243,-2.60437 -2.96885,0.11472 -23.4912,-1.90285 -31.41506,-2.52167 -8.19966,-0.64036 -7.07039,-0.18198 -16.229703,-0.79696 z",
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
        'eb_right':"m 169.9003,126.15476 c 12.84896,1.53048 25.28882,2.45467 35.15178,0" ,#"M169.9 126.155h35.152",
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,-24.37947 16.819944,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z"
    },
    {
        'id':2,
        'name':"sad",
        'mouth':"m 96.029224,210.17896 c 8.441896,-6.97268 18.309516,-13.95449 27.843836,-17.63182 3.58744,-1.33113 17.55481,-6.18499 21.34908,-6.12313 4.22117,-0.0132 19.81861,5.38315 21.89891,6.42613 11.61071,4.43883 20.13472,11.22679 29.13472,19.46698 -11.78149,-8.72469 -11.86217,-9.78333 -25.06561,-16.51813 -4.33334,-2.21034 -22.59321,-7.84542 -25.97284,-8.04015 -2.96885,0.11472 -17.77123,4.37283 -24.46975,7.51833 -9.76665,4.58625 -12.98408,7.03549 -24.718346,14.90179 z" ,
        'eb_left':"m 85.422617,126.15477 c 8.830391,3.29868 19.312573,12.52967 35.151783,0",
        'eb_right':"m 169.9003,126.15476 c 10.61618,6.97353 21.55612,11.89655 35.15178,0",
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,8.76195 16.819944,8.76195 9.2894,0 16.81994,-22.22636 16.81994,-8.76195 z" ,
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.24706,9.20757 16.53646,9.20757 9.2894,0 17.10342,-22.67197 17.10342,-9.20757 z",
    }
    ,
    { 
        'id':3,
        'name': "hearth",
        'mouth':"m 138.88292,214.70953 c 0.29018,0.8923 0.73034,2.66914 2.94324,4.51457 1.13812,0.7337 1.71617,1.26725 4.70458,2.55054 3.18718,-1.09241 4.35076,-1.59128 5.16825,-2.26725 2.32008,-1.791 2.63783,-3.77683 3.01839,-4.6003 0.76394,-2.17464 -1.25519,-5.94491 -4.37523,-5.95313 -1.83622,-0.005 -3.43527,2.74021 -3.51653,3.87374 -0.18418,-0.82611 -1.92366,-3.93027 -4.46815,-3.89235 -2.47016,0.0368 -3.95468,3.65146 -3.47455,5.77418 z",
        'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
       'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,-14.19189 -16.15268,-14.19189 -7.80991,0 -14.3766,24.03488 -16.2702,13.57604 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
      'eye_right':"m 203.91816,159.79463 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.68587,-13.90841 -16.34167,-13.90841 -7.80991,0 -14.18761,23.7514 -16.08121,13.29256 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z"
    },
    {
        'id':4,
        'name':"wink",
        'mouth':"m 91.711557,197.0722 c 11.182233,-0.21635 9.309533,11.81226 20.234543,13.93646 8.66395,1.26745 9.78694,1.55259 17.18005,2.13825 9.13486,0.55376 5.1587,0.23174 14.98751,0.89674 14.16117,0.38312 17.59856,0.39821 18.57075,2.06747 -10.73573,0.026 -12.00877,-0.21798 -18.72118,-0.11319 -5.29009,0.0826 -15.11861,-0.67907 -18.49824,-0.8738 -3.06239,-0.16591 -11.16686,-0.60936 -18.97367,-2.10072 -8.199657,-1.5664 -5.62045,-15.33623 -14.779763,-15.95121 z" ,
        'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
        'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
        'eye_left':"m 121.29728,159.58913 c -0.0143,2.36869 -1.37809,4.07896 -5.52898,5.64727 -13.07005,4.93819 -17.409562,4.61818 -22.139519,6.1363 -4.728294,1.51759 -5.224377,-1.34308 -3.625335,-2.85344 0.519994,-0.49116 28.012874,-6.48054 26.725034,-8.45057 -7.44858,-11.39419 -25.928037,-10.16916 -27.933518,-11.37211 -8.879725,-5.32634 32.583468,-2.56653 32.502318,10.89255 z"  ,
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z",
    },
    {
        'id':5,
        'name':"angry",
        'mouth':"m 111.26358,221.58814 c 6.03316,-8.98786 13.08523,-17.98748 19.8991,-22.7276 2.56383,-1.71584 12.54586,-7.97251 15.25751,-7.89278 3.01673,-0.017 14.16372,6.93894 15.65045,8.28334 8.2978,5.7217 14.38964,14.47145 20.82165,25.09315 -8.41985,-11.24623 -8.47751,-12.61081 -17.91359,-21.29205 -3.0969,-2.84914 -16.14664,-10.11282 -18.56196,-10.36383 -2.12174,0.14788 -12.70053,5.63662 -17.48775,9.6912 -6.97991,5.91174 -9.2793,9.06882 -17.66541,19.20857 z" ,
        'eb_right':"m 166.96034,130.96561 c 10.50128,6.54269 22.0775,-1.98396 38.09174,-4.81085" ,
        'eb_left':"m 87.57119,127.94781 c 6.142657,-0.15429 27.89735,10.94465 37.28994,2.67269",
        'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,17.55811 -16.15268,17.55811 -7.809906,0 -14.376598,-7.71512 -16.270204,-18.17396 -0.358721,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -2e-6,-13.46441 7.530545,-24.37947 16.819944,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
        'eye_right':"m 203.91816,159.79463 c 0,2.22245 -0.20517,4.37545 -0.58956,6.42136 -1.94436,10.34897 -8.4743,17.95811 -16.23038,17.95811 -7.49813,0 -13.85032,-7.11143 -16.02129,-16.93483 -0.51864,-2.34676 -0.79865,-4.8483 -0.79865,-7.44464 0,-13.4644 7.53054,-24.37946 16.81994,-24.37946 9.2894,0 16.81994,10.91506 16.81994,24.37946 z",
    },
    #DON'T KNOW IF TO KEEP IT OR NOT. Not so happy about the visual of  mortphing of the mouth
    {
      'id':6,
      'name':"smile3",
      'mouth':"m 154.44536,202.76723 c -1.31564,0.84624 -5.6355,-2.15409 -8.84524,-6.98482 -5.83673,-8.78441 -15.1141,-20.44179 -14.05943,0.20105 -0.0191,5.1224 9.57274,9.07482 9.6346,12.86909 -0.0132,4.22117 -9.43021,3.88374 -9.36419,9.57183 0.072,10.4586 12.01739,4.38482 22.2725,1.99933 -3.80068,-4.28984 -18.69837,7.38698 -21.06171,-0.47682 -1.40009,-4.65866 10.04821,-7.48855 9.85348,-10.86818 0.11472,-2.96885 -13.39533,-13.27115 -9.11919,-19.40424 6.05026,-8.67766 12.48879,16.67531 20.68918,13.09276 z",
      'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
      'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
     'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,-14.19189 -16.15268,-14.19189 -7.80991,0 -14.3766,24.03488 -16.2702,13.57604 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
      'eye_right':"m 203.91816,159.79463 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.68587,-13.90841 -16.34167,-13.90841 -7.80991,0 -14.18761,23.7514 -16.08121,13.29256 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z"
    },

     #DON'T KNOW IF TO KEEP IT OR NOT
    {
       'id':7,
       'name':"bigsmile",
       'mouth':"m 97.3423,213.19999 c 8.4419,6.97268 18.84406,16.35992 28.37838,20.03725 3.58744,1.33113 17.55481,6.18499 21.34908,6.12313 4.22117,0.0132 19.81861,-5.38315 21.89891,-6.42613 11.61071,-4.43883 20.04023,-11.51027 29.04023,-19.75046 -13.33787,0.0627 -7.08236,-0.026 -22.73847,-0.0526 -4.8645,-0.008 -24.82586,-0.15646 -28.20549,0.0383 -2.96885,-0.11472 -20.94487,0.0207 -28.34515,0.032 -15.7134,0.0241 -6.30235,0.0472 -21.37749,-0.001 z",
       'eb_right':"m 169.90029,126.15476 c 11.71726,-15.67218 23.43453,-14.55742 35.15179,0" ,
      'eb_left':"m 85.422617,126.15477 c 11.717261,-15.67218 23.434523,-14.55742 35.151783,0" ,
      'eye_left':"m 121.33035,159.60567 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.49688,-14.19189 -16.15268,-14.19189 -7.80991,0 -14.3766,24.03488 -16.2702,13.57604 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z",
      'eye_right':"m 203.91816,159.79463 c 0,2.36779 -0.23288,4.65674 -0.66726,6.82135 -2.03571,10.14445 -8.68587,-13.90841 -16.34167,-13.90841 -7.80991,0 -14.18761,23.7514 -16.08121,13.29256 -0.35872,-1.98131 -0.54974,-4.06107 -0.54974,-6.2055 -1e-5,-13.46441 7.53054,-24.37947 16.81994,-24.37947 9.2894,0 16.81994,10.91506 16.81994,24.37947 z" ,  

    }
    
]
# Default route to /
@app.route("/")
def index():
    return "Hello Flask!"

#Getting all the API data in face/all
@app.route('/face/all', methods=['GET'])
def faces():
    return jsonify(face_data)



#Example of URL
# http://YOUR-LOCALHOST/face?name=smile
@app.route('/face',methods=['GET']) 
def get_name():
    if 'name' in request.args:
        name=str(request.args['name'])
    else:
        return "ERROR: Name needed"

    results = []
    for face in face_data:
        if face['name'] == name:
            results.append(face)

    # convert list of Python dictionaries to the JSON format
    return jsonify(results)


if __name__ == "__main__":
        app.run()