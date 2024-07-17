# import sys
# from PySide6.QtCore import Qt
# from PySide6.QtGui import QIcon, QFont, QAction
# from PySide6.QtWidgets import QApplication, QLabel, QMenu, QWidget
#
#
#
# class MyWin(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         # self._createActions()  # +++
#
#         # self.label = QLabel("Hello, World", self, font=QFont("Calibri", 20))
#         # # self.label.setAlignment(Qt.WidgetAttribute.AlignCenter)
#         # self.label.resize(300, 300)
#         # self.label.setStyleSheet('''background-color: grey;
#         #                     border: 2px solid #f00;
#         #                     border-radius: 10px;
#         #                     ''')
#
#         # self._menu.setWindowFlags(Qt.WindowType.FramelessWindowHint)
#         # self._menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
#         # self.resize(self.label.width(), self.label.height())
#
#         # +++ vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
#         self._menu = QMenu()
#         self._menu.setWindowFlags(Qt.WindowType.FramelessWindowHint)
#         self._menu.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
#         self._menu.setStyleSheet("""QMenu{
#                   background-color: rgb(255, 255, 255);
#                   border-radius: 10px;
#                   border: 2px solid red;
#             }""")
#         self.newAction = QAction(self)
#         self.newAction.setText("&New")
#         newAct = self._menu.addAction(self.newAction)
#         # openAct = self._menu.addAction(self.openAction)
#         # self._menu.addSeparator()
#         # quitAct = self._menu.addAction(self.exitAction)
#
#         # QApplication.instance().focusObjectChanged.connect(self.focusChanged)########
#         # self._connectActions()
#
#     # def _createActions(self):
#     #     s
#         # self.newAction.setIcon(QIcon("img/new.png"))
#         # self.openAction = QAction(QIcon("img/open.png"), "&Open...", self)
#         # self.exitAction = QAction(QIcon("img/exit.png"), "&Quit", self)
#
#     # def focusChanged(self, obj):
#     #     if not obj or obj.window() == self.window():
#     #         self._menu.hide()
#
#     def contextMenuEvent(self, event):
#         self._menu.hide()
#         action = self._menu.exec(self.mapToGlobal(event.pos()))
#
#     # def _connectActions(self):
#     #     # self.newAction.triggered.connect(self.newFile)
#     #     # self.openAction.triggered.connect(self.openFile)
#     #     self.exitAction.triggered.connect(self.close)
#
#     # def newFile(self):
#     #     self.label.setText("<b>File > <i style='color: red'>New...</i></b> clicked")
#     #     self._menu.hide()
#     #
#     # def openFile(self):
#     #     self.label.setText("<b>File > <i style='color: red'>Open...</i></b> clicked")
#     #     self._menu.hide()
#
#
# # +++ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = MyWin()
#     w.show()
#     sys.exit(app.exec())
# def threeSum( nums):
#     out = []
#     len_ = len(nums)
#     for i in range(0, len_ - 2, 3):
#         for y in range(i + 1, len_ - 1, 2):
#             for z in range(y + 1, len_):
#                 if nums[i] + nums[y] + nums[z] == 0:
#                     out.append([nums[i], nums[y], nums[z]])
#     tmp = []
#     for i in range(len(out)):
#         if out[i] == tmp:
#             del out[i]
#             continue
#         tmp = out[i]
#
#     return out
# print(threeSum([-2,0,1,1,2]))
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
drt = TreeNode(1, TreeNode(2), TreeNode(4))
def hasPathSum( root, targetSum: int) -> bool:
    if root != None:
        targetSum = targetSum - root.val

        if targetSum == 0:
            return True
        if hasPathSum(root.left, targetSum):
            return True
        if hasPathSum(root.right, targetSum):
            return True

    return False



print(hasPathSum(drt, 5))