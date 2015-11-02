/****************************************************************************
 * GenerateRPN.cc
 *
 * A c++ test project
 * Generate reverse polish notation for a given math notation.
 *
 * Example:
 *
 * (a+b)*c => ab+c*
****************************************************************************/

#include <stdio.h>
#include <iostream>
#include <map>
#include <stack>
#include <string.h>

using namespace std;

map<char, int> opPiority;
char * generateRPN( char *mathNotation );

int main(){
    //
    opPiority['+'] = 1;
    opPiority['-'] = 1;
    opPiority['*'] = 2;
    opPiority['/'] = 2;
    
    while(true){
        cout<<"Please input the mathNotation, if wanna quit input 'quit'."<<endl;
        char mathNotation[1024] = {0};
        cin>>mathNotation;
        if( 0==strcmp(mathNotation,"quit") ){
            break;
        }else{
            cout<<generateRPN( mathNotation )<<endl;    
        }
    }
    return 0; 
}

char * generateRPN( char *mathNotation ){
    //
    if( NULL == mathNotation ){
        return NULL;
    }

    int notationLen = strlen(mathNotation);
    if( 0 == notationLen ){
        return NULL;
    }

    char *retRPN = new char( notationLen );
    memset( retRPN, 0, notationLen );
    stack<char> stackNum;
    stack<char> stackOperator;

    for( int i=0; i<notationLen; i++ ){
        //
        if( '(' == mathNotation[i] ){
            stackOperator.push( mathNotation[i] );
        }else if( ')' == mathNotation[i] ){
            while( !stackOperator.empty() && '(' != stackOperator.top() ){
                stackNum.push( stackOperator.top() );
                stackOperator.pop();
            }
            stackOperator.pop();
        }else if( opPiority.find( mathNotation[i] ) != opPiority.end() ){
            if( stackOperator.empty() || '('==stackOperator.top() ){
                stackOperator.push( mathNotation[i] );
            }else{
                while( !stackOperator.empty() && opPiority[stackOperator.top()]>=opPiority[mathNotation[i]] ){
                    stackNum.push( stackOperator.top() );
                    stackOperator.pop();
                }
                stackOperator.push( mathNotation[i] );
            }
        }else{
            stackNum.push( mathNotation[i] );
        }
        
    }

    int index = stackNum.size();
    int numIndex = index;
    
    while( !stackNum.empty() ){
        retRPN[--numIndex] = stackNum.top();
        stackNum.pop();
    }

    while( !stackOperator.empty() ){
        retRPN[index++] = stackOperator.top();
        stackOperator.pop();
    }

    return retRPN;

}





