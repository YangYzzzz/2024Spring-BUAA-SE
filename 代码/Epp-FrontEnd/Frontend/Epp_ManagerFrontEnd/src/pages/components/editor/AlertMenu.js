import Editor from 'wangeditor' // npm 安装
const { $, BtnMenu, DropListMenu, PanelMenu, DropList, Panel, Tooltip } = Editor
var _this = null
export  default class AlertMenu extends BtnMenu {
  constructor(editor) {
    // data-title属性表示当鼠标悬停在该按钮上时提示该按钮的功能简述
    _this = editor
    const $elem = Editor.$(
      `<div class="w-e-menu" data-title="Alert">
                <button>alert</button>
            </div>`
    )
    super($elem, editor)
  }
  // 菜单点击事件
  clickHandler() {
    // 做任何你想做的事情
    // 可参考【常用 API】文档，来操作编辑器
    let selectionText = _this.selection.getSelectionText()
    let SelectionContainerElem  = _this.selection.getSelectionEndElem().elems[0]
    console.log(SelectionContainerElem)

    _this.cmd.do('fontSize', '36px')
    // _this.cmd.do('insertHTML', '<h1>selectionText</h1>')

  }
  // 菜单是否被激活（如果不需要，这个函数可以空着）
  // 1. 激活是什么？光标放在一段加粗、下划线的文本时，菜单栏里的 B 和 U 被激活，如下图
  // 2. 什么时候执行这个函数？每次编辑器区域的选区变化（如鼠标操作、键盘操作等），都会触发各个菜单的 tryChangeActive 函数，重新计算菜单的激活状态
  tryChangeActive() {
    // 激活菜单
    // 1. 菜单 DOM 节点会增加一个 .w-e-active 的 css class
    // 2. this.this.isActive === true
    this.active()

    // // 取消激活菜单
    // // 1. 菜单 DOM 节点会删掉 .w-e-active
    // // 2. this.this.isActive === false
    // this.unActive()
  }
}

