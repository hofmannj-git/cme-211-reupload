import sys
import time
import math

def adj_cos_sim(movieA, movieB, func_1, user_thresh):
    """ This function takes in the three arguments "movieA" and "movieB", \
        which specify which two movies should be compared, "func_1", which is \
        the tuple containing the output data from all movies and users, and \
        "user_thresh", which sets the minimum number of common users. It then \
        calculates the adjusted cosine similarity for those two movies. It \
        outputs the data in the desired format. \n
        'P_ab' = the adjusted cosine similarity parameter between the two \
        movies of interest \n
        'numcommonusers' = the number of users rating both movies A & B \n """
    
    # unpacks the tuple of data within the function
    movie_user_dict, movielist_sort, movie_avg_rating, user_rating_dict, \
        N_users, N_movies, N_lines = func_1
    
    # determines users who have rated both movies in question
    setofusers = movie_user_dict[movieA].intersection(movie_user_dict[movieB])
    tupleofusers = tuple(setofusers)
    numcommonusers = len(tupleofusers)

    if numcommonusers < user_thresh:
        P_ab = "NO COMP"
    else:
        for i in range(1,numcommonusers+1):
            usernum = tupleofusers[i-1]
            avg_movA = movie_avg_rating[movieA]
            avg_movB = movie_avg_rating[movieB]
            rating_movA = user_rating_dict[usernum][movieA]
            rating_movB = user_rating_dict[usernum][movieB]
            if i==1:
                sumdiff = (rating_movA - avg_movA)*(rating_movB - avg_movB)
                sumra2 = (rating_movA - avg_movA)**2
                sumrb2 = (rating_movB - avg_movB)**2
            else:
                sumdiff += (rating_movA - avg_movA)*(rating_movB - avg_movB)
                sumra2 += (rating_movA - avg_movA)**2
                sumrb2 += (rating_movB - avg_movB)**2
        if math.isclose(0,math.sqrt(sumra2*sumrb2)):
            P_ab = "NO COMP"
        else:
            P_ab = sumdiff/math.sqrt(sumra2*sumrb2)

    return P_ab, numcommonusers


def checkforsimilarities(movieA, movieB, func_2, movie_similarities):
    """ This function takes in the arguments "movieA" & "movieB" which specify \
        the two movies of interest, and "func_2" which contains the outputs \
        from the calculation of the adjusted cosine similarity. It outputs: \n
        'movie_similarities' = a dict of movies as keys containing a list \
        (movie ID of similarity, coefficient, number of common users) with the \
        most related movie, if any. \n """
    
    P_ab, numcommonusers = func_2 # unpack tuple input
    
    if P_ab != "NO COMP":
        if movieA in movie_similarities:
            if P_ab > movie_similarities[movieA][1]:
                movie_similarities[movieA] = [movieB, P_ab, numcommonusers]
        else:
            movie_similarities[movieA] = [movieB, P_ab, numcommonusers]
        if movieB in movie_similarities:
            if P_ab > movie_similarities[movieB][1]:
                movie_similarities[movieB] = [movieA, P_ab, numcommonusers]
        else:
            movie_similarities[movieB] = [movieA, P_ab, numcommonusers]

    return movie_similarities


def loadformatdata(data_file):
    """ This function takes in the argument "data_file" which specifies the \
        desired data input file to read. It outputs the data in the desired \
        formats. \n
        'movie_user_dict' = a dict of movies as keys containing a set of users \
        who rated each movie \n
        'movielist_sort' = a sorted list of all movies indices \n
        'movie_avg_rating' = a dictionary of the average rating of movies \n
        'user_rating_dict' = a dict of users as keys containing a dict of the \
        movies they rated (key) with the rating (value) \n
        'N_users' = the number of unique users who rated movies \n
        'N_movies' = the number of unique movies that were rated \n
        'N_lines' = the total number of lines that were read \n """
    
    # reads in the data from data_file
    with open(data_file, 'r') as f:
        alllines = f.readlines()

    userlist = []
    movielist = []
    movie_user_dict = dict() # a dict w/ all movies (keys) with users (sets)
    movie_avg_rating = dict() # a dict w/ the avg. rating for each movie (key)
    movie_num_ratings = dict() # a dict w/ the number of ratings for each movie
    user_rating_dict = dict() # a dict w/ users & movie ratings

    count = 0
    for linenum in alllines:
        templine = alllines[count].split()
        line = templine[0:3]
        userint = int(line[0])
        movieint = int(line[1])
        ratingint = int(line[2])
        userlist.append(userint)
        movielist.append(movieint)
        count += 1
    
        # Adds user ID to set of users who rated given movie in dictionary
        if movieint in movie_user_dict:
            movie_user_dict[movieint].add(userint)
        else:
            movie_user_dict[movieint] = {userint}

        # Adds the rating to the total rating (used to calc. avg.) for movie
        if movieint in movie_avg_rating:
            movie_avg_rating[movieint] += ratingint
            movie_num_ratings[movieint] += 1
        else:
            movie_avg_rating[movieint] = ratingint
            movie_num_ratings[movieint] = 1

        # Adds the movie & rating to a dictionary under the given user
        if userint in user_rating_dict:
            user_rating_dict[userint][movieint] = ratingint
        else:
            user_rating_dict[userint] = {}
            user_rating_dict[userint][movieint] = ratingint
                
    for k, v in movie_avg_rating.items(): # calculates average for each movie
        movie_avg_rating[k] = v/movie_num_ratings[k]
    
    # Use set matching to find number of unique movies and users for printing
    userset = set(userlist)
    movieset = set(movielist)
    movielist_sort = list(movieset)
    movielist_sort.sort() # sorted list for later reference
    N_users = len(userset)
    N_movies = len(movieset)
    N_lines = len(alllines)

    return movie_user_dict, movielist_sort, movie_avg_rating, \
        user_rating_dict, N_users, N_movies, N_lines


def outputdata(output_file, N_movies, movie_similarities, movielist_sort):
    """ This function takes in the arguments for the similarity data, \ characteristics, and output file name, and writes to file in the \
        desired format. \n"""
    with open(output_file, 'w') as g:
        for m in range(1,N_movies+1): # cycles through movies, writes per line
            if m in movie_similarities:
                movie_simnum = movie_similarities[m][0]
                sim_coeff = movie_similarities[m][1]
                commonusers = movie_similarities[m][2]
                g.write("{} ({},{:0.2f},{})\n".format(movielist_sort[m-1], \
                                        movie_simnum, sim_coeff, commonusers))
            else:
                g.write("{}\n".format(movielist_sort[m-1]))



# ACTUAL BODY OF CODE (not functions)

if __name__ == "__main__": # Reads the command line inputs
    # if no arguments, prints usage message
    
    if len(sys.argv) <= 3:
        print("Usage:")
        print("  $ python3 similarity.py <data_file> <output_file> " \
              "[user_thresh (default = 5)]")
        sys.exit(0)
              
    # declares variables from input arguments
    data_file = sys.argv[1]
    output_file = sys.argv[2]
    user_thresh = int(sys.argv[3])

    inittime = time.time()

    print("Input MovieLens file: {}".format(data_file))
    print("Output file for similarity data: {}".format(output_file))
    print("Minimum number of common users: {}".format(user_thresh))

    # Runs load & data function and unpacks tuple output
    func_1 = loadformatdata(data_file)
    movie_user_dict, movielist_sort, movie_avg_rating, user_rating_dict, \
        N_users, N_movies, N_lines = func_1

    print("Read {} lines with total of {} movies and {} users" \
          .format(N_lines, N_movies, N_users))

    # Compares each movie, and formulates the desired output for each movie.
    movie_similarities = dict()
    for i in range(1,N_movies+1):
        for j in range(i+1,N_movies+1):
            # Uses functions (above) to calculate similarity coefficient and
            # check against existing coefficients to make best recommendation.
            func_2 = adj_cos_sim(i, j, func_1, user_thresh)
            movie_similarities = checkforsimilarities(i, j, func_2, \
                                                      movie_similarities)

    # Outputting calculated results
    outputdata(output_file, N_movies, movie_similarities, movielist_sort)

    finaltime = time.time()
    timeelapsed = finaltime - inittime

    print("Computed similarities in {:0.3f} seconds".format(timeelapsed))
