import java.util.Queue;
import java.util.Scanner;
import java.util.Stack;
import java.util.concurrent.LinkedBlockingQueue;

public class GenerateRPN {

	
	static String operator = "+-*/()";

	public static int opcompare(char op1, char op2) {
		if (op1 == '(') { 
			return 1;
		} else if ("+-".indexOf(op1) >= 0) {
			if ("+-".indexOf(op2) >= 0) {
				return 0;
			}
			return 1;
		} else // if("*/%".indexOf(op1) >=0) 
		{
			if ("+-".indexOf(op2) >= 0) {
				return -1;
			}
			return 0;
		}
	}
	public static String generateRPN(String s) throws Exception {
		LinkedBlockingQueue<String> polish = new LinkedBlockingQueue<String>();
		StringBuffer temp = new StringBuffer();
		
		Stack<Character> stack = new Stack<Character>();
		for (int i = 0; i < s.length(); i++) {

			char c = s.charAt(i);
			if (operator.indexOf(c) >= 0) {
				if (temp.length() > 0) {
					polish.offer(temp.toString());
					temp = new StringBuffer();
				}
				switch (c) {
				case '(':
					stack.push(c);
					break;
				case ')':
					while (stack.size() > 0) {
						char op = stack.pop();
						if (op != '(') {
							polish.offer(String.valueOf(op));
						} else {
							break;
						}
					}
					break;
				default:
					if (stack.size() == 0) {
						stack.push(c);
					} else {
						while (stack.size() > 0) {
							char op1 = stack.lastElement();
							int com = opcompare(op1, c);
							if (com <= 0) {
								polish.offer(String.valueOf(stack.pop()));
							} else {
								stack.push(c);
								break;
							}
						}
						if (stack.size() == 0) {
							stack.push(c);
						}
					}
					break;
				}
			} else {
				temp.append(c);
			}
		}
		if (temp.length() > 0) {
			polish.offer(temp.toString());
		}
		while (stack.size() > 0) {
			polish.offer(String.valueOf(stack.pop()));
		}

		return polish.toString();
	}
	
	
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub

		Scanner reader = new Scanner(System.in);
		while(true)
		{
            System.out.println("Please input the math notation, if you wanna quit, input 'quit':");
		    String s = reader.nextLine();
                if( s.equals("quit") ){
                    break;
                }
                String result = "";
		    try {
			    result = generateRPN(s);
		    }catch(Exception e) {
			    // TODO Auto-generated catch block
			    e.printStackTrace();
		    }
		    System.out.println(result);
		}
	}

}
