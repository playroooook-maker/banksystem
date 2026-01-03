extern "C"{
	int create_account_impl(int);
	int get_balance_impl(int);
	int transfer_impl(int,int,int,int*,int*);
	int core_create_account(int initial_balance){
		return create_account_impl(initial_balance);
	}
	int core_get_balance(int account_id){
		return get_balance_impl(account_id);
	}
	int core_transfer(int from_id,int to_id,int amount,int* new_balance_from,int* new_balance_to){
		return transfer_impl(from_id,to_id,amount,new_balance_from,new_balance_to);
	}
}
