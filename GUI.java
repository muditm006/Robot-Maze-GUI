import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import javax.swing.JButton;
import javax.swing.JFrame;
import clientpkg.clientpkg;

public class GUI extends JFrame implements ActionListener {
  String[] msgs = {"Left", "Right", "Forward", "Reverse"};
  JButton button1 = new JButton("Left");
  JButton button2 = new JButton("Right");
  JButton button4 = new JButton("Forward");
  JButton button5 = new JButton("Reverse");
  clientpkg client = new clientpkg();

  public GUI() {
    BorderLayout layout = new BorderLayout();
    setLayout(layout);
    button1.addActionListener(this);
    button2.addActionListener(this);
    button4.addActionListener(this);
    button5.addActionListener(this);
    add(button1, BorderLayout.WEST);
    add(button2, BorderLayout.EAST);
    add(button4, BorderLayout.NORTH);
    add(button5, BorderLayout.SOUTH);
    setDefaultCloseOperation(EXIT_ON_CLOSE);
    setSize(400, 200);
    setVisible(true);
  }

  @Override
  public void actionPerformed(ActionEvent e) {
    Object obj = e.getSource();
    if (obj == button1) {
      client.left();
    }
    if (obj == button2) {
      client.right();
    }
    if (obj == button4) {
      client.forward();
    }
    if (obj == button5) {
      client.reverse();
    }
  }

  public static void main(String[] args) {
    GUI app = new GUI();

  }

}
