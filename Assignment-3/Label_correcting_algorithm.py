'''
Shortest path in python.
'''
import csv

_MAX_LABEL_COST = 10000
g_node_list = []
g_agent_list = []
g_link_list = []
g_internal_node_id_dict = {}
g_external_node_id_dict = {}
g_number_of_nodes = 0
g_number_of_links = 0
g_number_of_agents = 0

g_node_status_array = []
g_node_label_cost = []
g_node_predecessor = []
g_link_predecessor= []


class Node:
        def __init__(self):
                self.node_id = 0           
                self.x = 0.0
                self.y = 0.0
                self.outgoing_node_list = []

class Link:
        def __init__(self):
                self.from_node_seq_no = 0
                self.to_node_seq_no = 0         
                self.travel_time = 0
                self.link_seq_no = 0
    
class Agent:
        def __init__(self):
                self.agent_id = 0
                self.origin_node_id = 0
                self.destination_node_id = 0
                self.path_cost = 0
                self.path_node_seq_no_list = []
                                
def g_ReadInputData():
        internal_node_seq_no = 0
        global g_number_of_agents 
        global g_number_of_nodes 
        global g_number_of_links 
        with open('input_node.csv','r') as fp:
                lines = fp.readlines()   
                for l in lines[1:]:
                        l = l.strip().split(',')  
                        try:
                                node = Node()
                                g_internal_node_id_dict[int(l[1])] = internal_node_seq_no
                                g_external_node_id_dict[internal_node_seq_no] = int(l[1])
                                node.node_id = internal_node_seq_no
                                internal_node_seq_no += 1
                                
#                                node.x = float(l[2])
#                                node.y = float(l[3])
                                
                                g_node_list.append(node)
                                g_number_of_nodes += 1
                                if g_number_of_nodes % 100 == 0:
                                        print('reading {} nodes..'\
                                                .format(g_number_of_nodes))
                        except:
                                print('Bad read. Check file your self')
                print('nodes_number:{}'.format(g_number_of_nodes))
        
        with open('input_link.csv','r') as fl:
                linel = fl.readlines()             
                for l in linel[1:]:
                        l = l.strip().split(',')
                        try:                                
                                link = Link()
                                link.link_seq_no = g_number_of_links
                                link.from_node_seq_no = g_internal_node_id_dict[int(l[0])]
                                link.to_node_seq_no = g_internal_node_id_dict[int(l[1])]                                
                                link.travel_time = float(l[2])
                                g_node_list[link.from_node_seq_no].outgoing_node_list.append(link) 
                                g_link_list.append(link)  
                                g_number_of_links += 1
                                
                                if g_number_of_links % 100 == 0:
                                        print('reading {} links..'\
                                                .format(g_number_of_links))   
                        except:
                                print('Bad read. Check file your self')
                print('links_number:{}'.format(g_number_of_links))
                                
        with open('input_agent.csv','r') as fa:
                linea = fa.readlines()
                for l in linea[1:]:
                        l = l.strip().split(',')
                        try:    
                                agent = Agent()
                                agent.agent_id = int(l[0])
                                agent.origin_node_id = g_internal_node_id_dict[int(l[1])]
                                agent.destination_node_id = g_internal_node_id_dict[int(l[2])]
                                agent.path_node_seq_no_list = []
                                agent.path_link_seq_no_list = []
                                g_agent_list.append(agent)
                                g_number_of_agents += 1
                        except:
                                print('Bad read. Check file your self')
                print('agents_number:{}'.format(g_number_of_agents))

def optimal_label_correcting(origin_node, destination_node):
        global _MAX_LABEL_COST
        global g_node_status_array
        global g_node_label_cost
        global g_node_predecessor
        global g_link_predecessor

        g_node_status_array=[0]*(g_number_of_nodes)
        g_node_label_cost=[_MAX_LABEL_COST]*(g_number_of_nodes)
        g_node_predecessor=[-1]*(g_number_of_nodes)
        g_link_predecessor=[0]*(g_number_of_nodes)

        if len(g_node_list[origin_node].outgoing_node_list) == 0:
                return _MAX_LABEL_COST

        g_node_label_cost[origin_node] = 0
        SEList = []
        SEList.append(origin_node)
               
        while len(SEList)>0:
                from_node = SEList[0]
                del SEList[0]
                g_node_status_array[from_node]=2

                for k in range(len(g_node_list[from_node].outgoing_node_list)):
                        link_no=g_node_list[from_node].outgoing_node_list[k].link_seq_no
                        to_node = g_node_list[from_node].outgoing_node_list[k].to_node_seq_no

                        if(g_node_label_cost[from_node]<_MAX_LABEL_COST-1):

                                new_to_node_cost = g_node_label_cost[from_node] + g_link_list[link_no].travel_time
                                
                                if (new_to_node_cost < g_node_label_cost[to_node]):  

                                        g_node_label_cost[to_node] = new_to_node_cost                                
                                        g_node_predecessor[to_node] = from_node  
                                        g_link_predecessor[to_node] = g_node_list[from_node].outgoing_node_list[k].link_seq_no  

                        if (g_node_status_array[to_node]==2):
                                continue

                        if(g_node_status_array[to_node]==0):
                                SEList.append(to_node)
                        
        if (destination_node >= 0 and g_node_label_cost[destination_node] < _MAX_LABEL_COST):
                return 1

        else: 
                return -1

def find_path_for_agents():

        global g_number_of_links
        global g_agent_list      
                
        for i in range(len(g_agent_list)):        
                g_agent_list[i].path_link_seq_no_list = []
                g_agent_list[i].path_node_seq_no_list = []
                
                return_value = optimal_label_correcting(g_agent_list[i].origin_node_id, g_agent_list[i].destination_node_id)

                if (return_value == -1):
                        print('agent ',i+1,'can not find destination node')
                        continue
                        
                current_node_seq_no = g_agent_list[i].destination_node_id
                g_agent_list[i].path_cost = g_node_label_cost[g_agent_list[i].destination_node_id]

                while (current_node_seq_no>=0):
                
                        current_link_seq_no = g_link_predecessor[current_node_seq_no]
                       
                        if(current_link_seq_no>=0):
                                g_agent_list[i].path_link_seq_no_list.append(current_link_seq_no)                                  
                                g_agent_list[i].path_node_seq_no_list.append(g_external_node_id_dict[current_node_seq_no])

                                current_node_seq_no = g_node_predecessor[current_node_seq_no]

        with open("output_agent.csv", "w") as output:
                output.write("agent_id,from_node,to_node,shortest_path_cost, shortest_path_node_seq\n")
                for i in range (0,len(g_agent_list)):
                        output.write('{},{},{},{},'.format(i+1,g_external_node_id_dict[g_agent_list[i].origin_node_id],g_external_node_id_dict[g_agent_list[i].destination_node_id],g_agent_list[i].path_cost))
                        for j in range (0,len(g_agent_list[i].path_node_seq_no_list)):
                                m=len(g_agent_list[i].path_node_seq_no_list)-1-j
                                output.write('{};'.format(g_agent_list[i].path_node_seq_no_list[m]))
                        output.write('\n')        

def output_path():
    for p_agent in g_agent_list:
        print('agent',p_agent.agent_id,' origin:',p_agent.origin_node_id,'destination:',p_agent.destination_node_id)
        route = 'route: ' + str(p_agent.path_node_seq_no_list[-1])
        for i in range(1,len(p_agent.path_node_seq_no_list)): route += ('-' + str(p_agent.path_node_seq_no_list[-i-1]))
        print(route)
        print('total cost:',p_agent.path_cost)
            
            
       
if __name__=='__main__':
        print('Reading data......')
        g_ReadInputData()
        print('Finding shortest path for all agents......')
        find_path_for_agents()     
        print('writing all agents path to output_agent.csv......')
        print('The shortest path finding is done!')   
        output_path()