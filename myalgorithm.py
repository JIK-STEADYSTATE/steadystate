from util import *

def algorithm(K, all_orders, all_riders, dist_mat, timelimit=60):

    start_time = time.time()

    for r in all_riders:
        r.T = np.round(dist_mat/r.speed + r.service_time)

    # A solution is a list of bundles
    solution = []

    #------------- Custom algorithm code starts from here --------------#
#==================  Customized util functions  ===============================
#==============================================================================
    def get_cheaper_available_riders(all_riders, rider, bundle):
        for r in all_riders:
            if r.available_number > 0 and r.fixed_cost+(bundle.total_dist/100)*r.var_cost < rider.fixed_cost+(bundle.total_dist/100)*rider.var_cost:
                return r
        
        return None
#===============================================================================
#===============================================================================
    car_rider = None
    for r in all_riders:
        if r.type == 'CAR':
            car_rider = r

    all_bundles = []

    for ord in all_orders:
        new_bundle = Bundle(all_orders, car_rider, [ord.id], [ord.id], ord.volume, dist_mat[ord.id, ord.id+K])
        all_bundles.append(new_bundle)
        car_rider.available_number -= 1

    best_obj = sum((bundle.cost for bundle in all_bundles)) / K
    print(f'Best obj = {best_obj}')

    # merge 가능성이 있는 order (주문 개수가 1개인 bundle을 의미)을 volume이 큰 순서대로 정렬한 list
    #left_bundle = sorted(all_bundles, key= lambda x: x.total_volume, reverse= True)
    left_bundle = sorted(all_bundles, key= lambda x: (all_orders[x.shop_seq[0]].deadline, x.total_volume), reverse= True)
    # greedy algorithm 욕심쟁이 알고리즘
    while True:
        if len(all_bundles) > 250 : 
            if len(left_bundle) == 0:
                break
            else:
                bundle1 = left_bundle.pop(0)
                #print(f"handle with {bundle1}")
            # for cur_bundle in left_bundle:
            for cur_bundle in left_bundle[:-round(len(left_bundle)/2)]:
                #print(f'try with bundle1: {bundle1}')
                bundle2 = cur_bundle
                #print(f'try to merge bundle2: {bundle2}')
                if (dist_mat[bundle2.shop_seq[0], bundle1.shop_seq[0]] + dist_mat[bundle2.shop_seq[0], bundle1.shop_seq[0] + K ]) / bundle1.rider.speed < all_orders[bundle1.shop_seq[0]].deadline : 
                
                    
                    new_bundle = try_merging_bundles(K, dist_mat, all_orders, bundle1, bundle2)
                    if new_bundle is not None:
                        #print(f'merge success!: {new_bundle}')
                        all_bundles.remove(bundle1)
                        bundle1.rider.available_number += 1
                        
                        all_bundles.remove(bundle2)
                        left_bundle.remove(bundle2)
                        bundle2.rider.available_number += 1
                        all_bundles.append(new_bundle)
                        bundle1 = new_bundle
                        new_bundle.rider.available_number -= 1
                        
                        
                        cur_obj = sum((bundle.cost for bundle in all_bundles)) / K
                        if cur_obj < best_obj:
                            best_obj = cur_obj
                            print(f'Best obj = {best_obj}')
                        else:
                            
                            pass
                            #print(f'left_num: {len(left_bundle)}')
                            #print(f'left_bundle: {left_bundle}')
                
                else :
                    pass

                if time.time() - start_time > timelimit:
                        break
        
        else : 
            if len(left_bundle) == 0:
                break
            else:
                bundle1 = left_bundle.pop(0)
                #print(f"handle with {bundle1}")
            # for cur_bundle in left_bundle:
            for cur_bundle in left_bundle:
                #print(f'try with bundle1: {bundle1}')
                bundle2 = cur_bundle
                #print(f'try to merge bundle2: {bundle2}')
                if (dist_mat[bundle2.shop_seq[0], bundle1.shop_seq[0]] + dist_mat[bundle2.shop_seq[0], bundle1.shop_seq[0] + K ]) / bundle1.rider.speed < all_orders[bundle1.shop_seq[0]].deadline : 
                
                    
                    new_bundle = try_merging_bundles(K, dist_mat, all_orders, bundle1, bundle2)
                    if new_bundle is not None:
                        #print(f'merge success!: {new_bundle}')
                        all_bundles.remove(bundle1)
                        bundle1.rider.available_number += 1
                        
                        all_bundles.remove(bundle2)
                        left_bundle.remove(bundle2)
                        bundle2.rider.available_number += 1
                        all_bundles.append(new_bundle)
                        bundle1 = new_bundle
                        new_bundle.rider.available_number -= 1
                        
                        
                        cur_obj = sum((bundle.cost for bundle in all_bundles)) / K
                        if cur_obj < best_obj:
                            best_obj = cur_obj
                            print(f'Best obj = {best_obj}')
                        else:
                            
                            pass
                            #print(f'left_num: {len(left_bundle)}')
                            #print(f'left_bundle: {left_bundle}')
                
                else :
                    pass

                if time.time() - start_time > timelimit:
                        break

        #if len(bundle1.shop_seq) == 1:
        #    left_bundle.append(bundle1)

        if time.time() - start_time > timelimit:
            break

        totaldistancelist = []
        for bundle in all_bundles:
            totaldistancelist.append(bundle.total_dist)
        
        totaldistancelist.sort(reverse=True)
        
        #print(totaldistancelist)


        sorted_all_bundles = sorted(all_bundles, key= lambda x : len(x.shop_seq), reverse= True)
        all_riders = sorted(all_riders, key = lambda x: (x.var_cost,x.fixed_cost), reverse= False)
        
        for bundle in sorted_all_bundles:
            new_rider = get_cheaper_available_riders(all_riders, bundle.rider, bundle)
            # if get_cheaper_available_riders(all_riders, bundle.rider, bundle) is not None:
            #     new_rider = get_cheaper_available_riders(all_riders, bundle.rider, bundle)
            #     old_rider = bundle.rider
            #     if try_bundle_rider_changing(all_orders, bundle, new_rider):
            #         old_rider.available_number += 1
            #         new_rider.available_number -= 1
                #print("new rider avail")
            if new_rider is not None:
                old_rider = bundle.rider
                if try_bundle_rider_changing(all_orders, dist_mat, bundle, new_rider):
                    old_rider.available_number += 1
                    new_rider.available_number -= 1

                if time.time() - start_time > timelimit:
                    break
            


        cur_obj = sum((bundle.cost for bundle in all_bundles)) / K
        if cur_obj < best_obj:
            best_obj = cur_obj
            print(f'Best obj = {best_obj}')

    # Solution is a list of bundle information
    solution = [
        # rider type, shop_seq, dlv_seq
        [bundle.rider.type, bundle.shop_seq, bundle.dlv_seq]
        for bundle in all_bundles
    ]
    #------------- End of custom algorithm code--------------#



    return solution