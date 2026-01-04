#include <unordered_map>
std::unordered_map<int,int> balances;
int next_account_id=1;
extern "C"{
	int create_account(int initial_balance){
		if(initial_balance<0)return-1;
		int id=next_account_id++;
		balances[id]=initial_balance;
		return id;
	}
	int get_balance(int account_id){
		if(!balances.count(account_id))return-1;
		return balances[account_id];
	}
	int transfer(int from_id,int to_id,int amount,int* new_from,int* new_to){
		if(amount<=0)return-1;
		if(!balances.count(from_id))return-2;
		if(!balances.count(to_id))return-3;
		if(balances[from_id]<amount)return-4;
		balances[from_id]-=amount;
		balances[to_id]+=amount;
		*new_from=balances[from_id];
		*new_to=balances[to_id];
		return 0;
	}
}

