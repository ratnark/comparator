import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from pandas._testing import assert_frame_equal
df1 = pd.read_csv('C:\\Users\\1787912\\Desktop\\GE_confidential\\19th March\\data extracts\\data extracts\\edl_csh_conc_spb_data.csv', encoding = 'utf-8')
df2 = pd.read_csv('C:\\Users\\1787912\\Desktop\\GE_confidential\\19th March\\data extracts\\data extracts\\t_df_csh_conc_spb_data.csv', encoding = 'utf-8')
notMatchingList = []
# convert_dict = {
#             'm251_cny_ppct_amt_driver': float
#            }
# df2 = df2.astype(convert_dict)


def dfTransformations(df1,df2):
    #filling NaN values with 0
    df1 = df1.fillna(0)
    df2 = df2.fillna(0)
    # df1 = df1.drop(['m251_cny_ppct_amt_driver'], axis = 1)
    # df2 = df1.drop(['m251_cny_ppct_amt_driver'], axis = 1)

    df1 = df1[df1.columns & df2.columns]
    df2 = df2[df1.columns & df2.columns]
    a = df1.sort_values(list(df1.columns))
    b = df2.sort_values(list(df2.columns))
    a.reset_index(drop=True, inplace=True)
    b.reset_index(drop=True, inplace=True)
    return [a,b]

edlAndTdf = dfTransformations(df1, df2)


def drop(i,b):
    b = b.drop([i])    
    b.reset_index(drop=True, inplace=True)
    return b

def testingFunction(a,b):
    print('Starting row by row testing \n')
    for i in range(len(a)):
        if a.iloc[i].equals(b.iloc[i]):
              print('matching',i)
        else:
            x =0
            if x == 0:
                print('******************************** not matching row number',i)
                print(a.iloc[i])
                print(b.iloc[i])
                notMatchingList.append([a.iloc[i],b.iloc[i]])
            else:
                #case one some of the rows have been removed from FDL side only,
                #this portion removes the same rows from other side also (set x =1)
                def multipleDeletion(a,b,i):
                    print('******************************** not matching row number',i)
                    print(a.iloc[i])
                    print(b.iloc[i])
                    b= drop(i, b)
                    print('dropping non matching row')
                    if a.iloc[i].equals(b.iloc[i]):
                        print('matching',i)
                        print(a.iloc[i])
                        print(b.iloc[i])
                    else:
                        print('************************recursion1')
                        multipleDeletion(a, b, i)
                multipleDeletion(a,b,i)
    print('Testing for ' + str(i) + ' rows completed')


# print(edlAndTdf[0]['rptg_dt'].unique(), edlAndTdf[1]['rptg_dt'].unique())
# print(len(edlAndTdf[0]), len(edlAndTdf[1]))

# print(assert_frame_equal(edlAndTdf[0][:50], edlAndTdf[1][:50]))

try:
    assert_frame_equal(edlAndTdf[0], edlAndTdf[1])
except:
    print("Something went wrong in data frame, check row by row")  
    testingFunction(edlAndTdf[0], edlAndTdf[1])
else:
    print("Both frames are identical")

# df5 = pd.DataFrame(np.random.random((10,3)), columns = ("col 1", "col 2", "col 3"))
# toCsv = [pd.DataFrame(notMatchingList[0][0]),pd.DataFrame(notMatchingList[0][1])]


# incasee frames are not identical run this to get result at desired address
# for item in range(len(notMatchingList)):
#     toCsv = [notMatchingList[item][0],notMatchingList[item][1]]
#     for df in toCsv:
#         with open('C:\\Users\\1787912\\Desktop\\example.csv','a',  encoding = 'utf-8') as f:
#             df.to_csv(f)
c = 0
dfList = []
for item in range(len(notMatchingList)):
    dfList.append(notMatchingList[item][0])
    dfList.append(notMatchingList[item][1])
    # dfList.append(pd.concat([pd.DataFrame(notMatchingList[item][0]),pd.DataFrame(notMatchingList[item][1])]))
    # dfList.append()
    # temp = pd.concat(dfList)
r = pd.DataFrame(pd.concat(dfList))
fig, ax =plt.subplots(figsize=(12,4))
ax.axis('tight')
ax.axis('off')
the_table = ax.table(cellText=r.values,colLabels=r.columns,loc='center')

#https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
pp = PdfPages("foo.pdf")
pp.savefig(fig, bbox_inches='tight')
pp.close()