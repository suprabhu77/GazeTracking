#include<stdio.h>
#include<string.h>
int main()
{
    char name[100];
    scanf("%[^\n]s",name);
    for(int i = 0;name[i]!='\0';i++)
    {
        if(name[i]>='a' && name[i]<='z')
        {
            name[i] = name[i] - 32;
        }
        else if(name[i]>='A' && name[i]<='z')
        {
            name[i] = name[i] + 32;
        }
    } 
    printf("%s",name);
}