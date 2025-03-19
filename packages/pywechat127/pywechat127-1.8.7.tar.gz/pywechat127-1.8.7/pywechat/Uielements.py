'''
Uielements
---------
PC微信中的各种Ui-Object
'''
#################################################################
#微信主界面:
#==========================================================================================
#工具栏 |搜索|       |+|添加好友              ···聊天信息按钮  #
#                                             |
#|头像|   |          |                            |
#|聊天|   |          |                            |
#|通讯录|  | 会话列表     |                            |
#|收藏|   |          |    聊天界面                    |
#|聊天文件| |          |                            |
#|朋友圈|  |          |                            |
#|视频号|  |          |                            |
#|看一看|  |          |                            |
#|搜一搜|  |          |                            |
#      |          |                            |
#      |          |                            |
#      |          |                            | 
#      |          |---------------------------------------------------------
#小程序面板 |          |  表情 聊天文件 截图 聊天记录           |
#|手机|   |          |                            |
#|设置及其他||          |                            |
#===========================================================================================
class Login_window():
    '''登录界面要用到的唯二的两个Ui:登录界面与进入微信按钮\n'''
    LoginWindow={'title':'微信','class_name':'WeChatLoginWndForPC','visible_only':False}
    LoginButton={'title':'进入微信','control_type':'Button'}

class ToolBar():
    '''主界面导航栏下的所有Ui'''
    Chat={'title':'聊天','control_type':'Button'}
    Contacts={'title':'通讯录','control_type':'Button'}
    Collections={'title':'收藏','control_type':'Button'}
    ChatFiles={'title':'聊天文件','control_type':'Button'}
    Moments={'title':'朋友圈','control_type':'Button'}
    Channel={'title':'视频号','control_type':'Button'}
    Topstories={'title':'看一看','control_type':'Button'}
    Search={'title':'搜一搜','control_type':'Button'}
    Miniprogram_pane={'title':'小程序面板','control_type':'Button'}
    SettingsAndOthers={'title':'设置及其他','control_type':'Button'}

    
class Main_window():
    '''主界面下所有的第一级Ui\n'''
    AddTalkMemberWindow={'title':'AddTalkMemberWnd','control_type':'Window','class_name':'AddTalkMemberWnd','framework_id':'Win32'}
    MainWindow={'title':'微信','class_name':'WeChatMainWndForPC'}
    Toolbar={'title':'导航','control_type':'ToolBar'}
    MessageList={'title':'会话','control_type':'List'}
    Search={'title':'搜索','control_type':'Edit'}
    SearchResult={'title_re':"@str:IDS_FAV_SEARCH_RESULT",'control_type':'List'}
    ChatToolBar={'title':'','found_index':0,'control_type':'ToolBar'}
    CurrentChatWindow={'control_type':'Edit','found_index':1}
    ProfileWindow={'class_name':"ContactProfileWnd",'control_type':'Pane','framework_id':'Win32'}
    FriendMenu={'control_type':'Menu','title':'','class_name':'CMenuWnd','framework_id':'Win32'}
    FriendSettingsWindow={'class_name':'SessionChatRoomDetailWnd','control_type':'Pane','framework_id':'Win32'}
    GroupSettingsWindow={'title':'SessionChatRoomDetailWnd','control_type':'Pane','framework_id':'Win32'}    
    SettingsMenu={'class_name':'SetMenuWnd','control_type':'Window'}
    ContactsList={'title':'联系人','control_type':'List'}
    SearchNewFriendBar={'title':'微信号/手机号','control_type':'Edit'}
    SearchNewFriendResult={'title_re':'@str:IDS_FAV_SEARCH_RESULT','control_type':'List'}
    AddFriendRequestWindow={'title':'添加朋友请求','class_name':'WeUIDialog','control_type':'Window','framework_id':'Win32'}
    AddMemberWindow={'title':'AddMemberWnd','control_type':'Window','framework_id':'Win32'}
    DeleteMemberWindow={'title':'DeleteMemberWnd','control_type':'Window','framework_id':'Win32'}
    Tickle={'title':'拍一拍','control_type':'MenuItem'}
    SelectContactWindow={'title':'','control_type':'Window','class_name':'SelectContactWnd','framework_id':'Win32'}
    SetTag={'title':'设置标签','framework_id':'Win32','class_name':'StandardConfirmDialog'}
    FriendChatList={'title':'消息','control_type':'List'}
    CantSendEmptyMessageTips={'title':'不能发送空白信息','control_type':'Text'}

class Independent_window():
    '''独立于微信主界面,将微信主界面关闭后仍能在桌面显示的窗口Ui\n'''
    Desktop={'backend':'uia'}#windows桌面
    SettingWindow={'title':'设置','class_name':"SettingWnd",'control_type':'Window'}#微信设置窗口
    ContactManagerWindow={'title':'通讯录管理','class_name':'ContactManagerWindow'}#通讯录管理窗口
    MomentsWindow={'title':'朋友圈','control_type':"Window",'class_name':"SnsWnd"}#朋友圈窗口
    ChatFilesWindow={'title':'聊天文件','control_type':'Window','class_name':'FileListMgrWnd'}#聊天文件窗口
    MiniProgramWindow={'title':'微信','control_type':'Pane','class_name':'Chrome_WidgetWin_0'}#小程序面板窗口
    SearchWindow={'title':'微信','class_name':'Chrome_WidgetWin_0','control_type':'Pane'}#搜一搜窗口
    ChannelWindow={'title':'微信','class_name':'Chrome_WidgetWin_0','control_type':'Pane'}#视频号窗口
    ContactProfileWindow={'title':'微信','class_name':'ContactProfileWnd','framework_id':'Win32','control_type':'Pane'}#添加新好友时的添加到通讯录窗口
    TopStoriesWindow={'title':'微信','class_name':'Chrome_WidgetWin_0','control_type':'Pane'}#看一看窗口
    ChatHistoryWindow={'control_type':'Window','class_name':'FileManagerWnd','framework_id':'Win32'}#聊天记录窗口
    GroupAnnouncementWindow={'title':'群公告','framework_id':'Win32','class_name':'ChatRoomAnnouncementWnd'}#群公告窗口
    NoteWindow={'title':'笔记','class_name':'FavNoteWnd','framework_id':"Win32"}#笔记窗口
    OldIncomingCallWindow={'class_name':'VoipTrayWnd','title':'微信'}#旧版本来电(视频或语音)窗口
    NewIncomingCallWindow={'class_name':'ILinkVoipTrayWnd','title':'微信'}#旧版本来电(视频或语音)窗口
    OldVoiceCallWindow={'title':'微信','class_name':'AudioWnd'}#旧版本接通语音电话后通话窗口
    NewVoiceCallWindow={'title':'微信','class_name':'ILinkAudioWnd'}#新版本接通语音电话后通话窗口
    OldVideoCallWindow={'title':'微信','class_name':'VoipWnd'}#新版本接通语音电话后通话窗口
    NewVideoCallWindow={'title':'微信','class_name':'ILinkVoipWnd'}#新版本接通视频电话后通话窗口
    OfficialAccountWindow={'title':'公众号','control_type':'Window','class_name':'H5SubscriptionProfileWnd'}#公众号窗口

class Buttons():
    '''
    微信界面内用到的的所有按钮\n
    '''
    CheckMoreMessagesButton={'title':'查看更多消息','control_type':'Button','found_index':1}#好友聊天界面内的查看更多消息按钮
    OfficialAcountButton={'title':'公众号','control_type':'Button'}#搜一搜内公众号按钮                                                                                                                                
    SettingsAndOthersButton={'title':'设置及其他','control_type':'Button'}#设置及其他按钮
    ConfirmQuitGroupButton={'title':'退出','control_type':'Button'}#确认退出群聊按钮
    CerateNewNote={'title':'新建笔记','control_type':'Button'}#创建一个新笔记按钮
    CerateGroupChatButton={'title':"发起群聊",'control_type':"Button"}#创建新群聊按钮
    AddNewFriendButon={'title':'添加朋友','control_type':'Button'}#添加新朋友按钮
    AddToContactsButton={'control_type':'Button','title':'添加到通讯录'}#添加群聊聊天界面至通讯录内按钮
    AcceptButton={'control_type':'Button','title':'接受'}#接听电话按钮
    ChatMessageButton={'title':'聊天信息','control_type':'Button'}#聊天信息按钮                   
    CloseAutoLoginButton={'control_type':'Button','title':'关闭自动登录'}#微信设置关闭自动登录按钮
    ConfirmButton={'control_type':'Button','title':'确定'}#确定操作按钮
    CancelButton={'control_type':'Button','title':'取消'}#取消操作按钮
    MultiSelectButton={'control_type':'Button','title':'多选'}#转发消息或文件时的多选按钮
    HangUpButton={'control_type':'Button','title':'挂断'}#接听语音或视频电话按钮
    SendButton={'control_type':'Button','title':'发送'}#转发文件或消息按钮
    SendRespectivelyButton={'control_type':'Button','title_re':'分别发送'}#转发消息时分别发送按钮
    SettingsButton={'control_type':'Button','title':'设置'}#工具栏打开微信设置menu内的选项按钮
    ClearChatHistoryButton={'control_type':'Button','title':'清空聊天记录'}#清空好友或群聊聊天记录时的按钮
    RestoreDefaultSettingsButton={'control_type':'Button','title':'恢复默认设置'}#微信设置回复默认设置
    VoiceCallButton={'control_type':'Button','title':'语音聊天'}#给好友拨打语音电话按钮
    VideoCallButton={'control_type':'Button','title':'视频聊天'}#给好友拨打视频电话按钮
    CompleteButton={'control_type':'Button','title':'完成'}#完成按钮
    PinButton={'control_type':'Button','title':'置顶'}#将好友置顶按钮
    CancelPinButton={'control_type':'Button','title':'取消置顶'}#取消好友置顶按钮
    TagEditButton={'control_type':'Button','title':'点击编辑标签'}#编辑好友或群聊标签按钮
    ChatHistoryButton={'control_type':'Button','title':'聊天记录'}#获取聊天记录按钮
    ChangeGroupNameButton={'control_type':'Button','title':'群聊名称'}#修改群聊名称按钮
    MyNicknameInGroupButton={'control_type':'Button','title':'我在本群的昵称'}#修改群内我的昵称按钮
    RemarkButton={'control_type':'Button','title':'备注'}#修改群聊备注时的按钮
    QuitGroupButton={'control_type':'Button','title':'退出群聊'}#退出某个群聊时的按钮
    DeleteButton={'control_type':'Button','title':'删除'}#将好友从群聊删除时界面内的按钮
    EditButton={'control_type':'Button','title':'编辑'}#编辑群公告内已有内容时下方的按钮
    EditGroupNotificationButton={'control_type':'Button','title':'点击编辑群公告'}#编辑群公告按钮
    PublishButton={'control_type':'Button','title':'发布'}#编辑群公告完成后发布群公告的发布按钮
    ContactsManageButton={'title':'通讯录管理','control_type':'Button'}#通讯录管理按钮
    ConfirmEmptyChatHistoryButon={'title':'清空','control_type':'Button'}#点击清空聊天记录后弹出的query界面内的清空按钮
    MoreButton={'title':'更多','control_type':'Button'}#打开微信好友设置界面更多按钮
