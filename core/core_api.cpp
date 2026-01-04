extern "C"{
	int create_account(int);
	int get_balance(int);
	int transfer(int,int,int,int*,int*);
	int core_create_account(int initial_balance){
		return create_account(initial_balance);
	}
	int core_get_balance(int account_id){
		return get_balance(account_id);
	}
	int core_transfer(int from_id,int to_id,int amount,int* new_balance_from,int* new_balance_to){
		return transfer(from_id,to_id,amount,new_balance_from,new_balance_to);
	}
}

