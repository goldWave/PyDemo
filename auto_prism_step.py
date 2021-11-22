# -*- coding: utf-8 -*-

import subprocess, time, sys
import uiautomation as auto

auto.uiautomation.SetGlobalSearchTimeout(2)  # 设置全局搜索超时 15
nshopLoginId = "PLSMainView.body.channelsArea.ChannelsArea.MidFrame.ChannelScrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.AddFrame.DefaultPlatformsAddList.ContentFrame.Naver Shopping LIVE"
channelCapsuleId = "PLSMainView.body.channelsArea.ChannelsArea.MidFrame.ChannelScrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.NormalDisFrame.CapsulesFrame.ChannelCapsule"
name_nshopping = "Naver Shopping LIVE"

def print(*objects, sep=' ', end='\n', file=sys.stdout, flush=True):
	__builtins__.print(*objects, sep=sep, end=end, file=file, flush=flush)


def checkNotice(_parWidget):
	_noticeWindow = _parWidget.WindowControl(searchDepth=1, ClassName="PLSAlertView")
	while True:
		if not _noticeWindow.Exists():
			return

		_id = _noticeWindow.AutomationId
		_msg = _noticeWindow.TextControl(AutomationId=_id + ".contentBorder.content.message")
		print("click notice content: %s" % _msg.GetLegacyIAccessiblePattern().Name)

		_noticeBox = _noticeWindow.GroupControl(AutomationId=_id+ '.contentBorder.content.widget.buttonBox')
		_btn = _noticeBox.ButtonControl(searchpath=1)
		print("click btn: " + _btn.Name)
		_btn.Click()

def toLogin(_url, _id_ui, _pw_ui, _login_btn) -> True:
        # _plat = getPlatform(_url)
        # print('found %s login page' % _plat)
        # _id, _pw = getusername(_plat)
        _id = "xxx"
        _pw = 'xxx'
        if _id == '' or _pw == '':
            print('acccout or password is empty')
            time.sleep(4)
            return

        try:
            _id_ui.Click()
            _id_ui.GetValuePattern().SetValue(_id)
        except:
            print("id except got it")

        try:
            _pw_ui.Click(simulateMove=False)
            _pw_ui.GetValuePattern().SetValue(_pw)
        except:
            print("pwd except got it")

        _login_btn.Click()

        print('maybe succeed...\ntry next...')
        time.sleep(2)
        return True


def clickTerms() -> bool:
	global prismWindow
	time.sleep(2)
	PLSNaverShoppingTerm  = prismWindow.WindowControl(searchDepth=1, AutomationId='PLSMainView.PLSNaverShoppingTerm')
	print(PLSNaverShoppingTerm.Name)
	_agrrenBtn = PLSNaverShoppingTerm.ButtonControl(AutomationId='PLSMainView.PLSNaverShoppingTerm.contentBorder.content.confirmButton')
	#click agreebtn
	_agrrenBtn.Click()

	#note page
	time.sleep(1)
	PLSNaverShoppingTerm.Refind()
	
	_tip = prismWindow.TextControl(AutomationId="PLSMainView.PLSNaverShoppingTerm.contentBorder.content.topTitleLabel")
	print(_tip.Name)
	if "Please check before starting a live stream." != _tip.Name:
		print('tip is not right')
		return False

	_agrrenBtn.Refind()
	_agrrenBtn.Click()

	checkNotice(prismWindow)
	return True

def nshoppingLogin() -> bool:
	global prismWindow
	time.sleep(2)
	prismWindow.ButtonControl(AutomationId=nshopLoginId).Click()
	login_page = prismWindow.WindowControl(searchDepth=1, AutomationId='PLSMainView.PLSBrowserView')
	time.sleep(5)
	#found click login type page
	_windget = login_page.GroupControl(searchDepth=1, ClassName='QCefWidgetImpl').PaneControl(searchDepth=3, ClassName='Chrome_WidgetWin_0')
	_document = _windget.DocumentControl(searchDepth=1)
	_url = _document.GetValuePattern().Value

	if _url.endswith('.shoppinglive.naver.com/'):
		_btn = _document.CustomControl(searchDepth=2, AutomationId='root').GroupControl(searchDepth=2, AutomationId='content').HyperlinkControl(searchDepth=1, foundIndex=1)
		_btn.Click()


	time.sleep(2)
	_windget.Refind()
	#found login password page
	_windget_1 = login_page.WindowControl(searchDepth=1, ClassName='QPLSBrowserPopupDialog').GroupControl(searchDepth=1, ClassName='QCefWidgetImpl').PaneControl(searchDepth=3, ClassName='Chrome_WidgetWin_0')
	_document = _windget_1.DocumentControl(searchDepth=1)
	_url = _document.GetValuePattern().Value
	print(_url)
	if not _url.startswith('https://nid.naver.com/nidlogin.login?'):
		return False

	print('found naver page')
	_sign_in_group = _document.CustomControl(searchDepth=2, AutomationId='container').CustomControl(searchDepth=1, AutomationId='frmNIDLogin')
	_id_input = _sign_in_group.EditControl(AutomationId='id')
	_pw_input = _sign_in_group.EditControl(AutomationId='pw')
	_btn = _sign_in_group.ButtonControl(AutomationId='log.login')

	isSucceed = toLogin(_document.GetValuePattern().Value,_id_input, _pw_input, _btn)
	if isSucceed == False:
		print('login failed')
		return False

	return clickTerms()

def clickCenterMenuItem(_menu):
	pRect = _menu.BoundingRectangle
	_menu.Click(x = int(pRect.width()*0.5), y = int(0.5*pRect.height()))



if __name__ == '__main__':
	subprocess.Popen(r'C:\Users\Administrator\AppData\Local\PRISMLiveStudio\PRISMLiveStudio.exe')
	time.sleep(10)
	_root = auto.GetRootControl()
	prismWindow = _root.WindowControl(searchDepth=1, AutomationId='PLSMainView')
	prismWindow.SetActive()

	# auto.EnumAndLogControl(xx)
	if nshoppingLogin() == False:
		print('login nshopping failed')
		exit(1)


	nshoppingChannel =  prismWindow.CustomControl(AutomationId=channelCapsuleId, Name=name_nshopping)
	if not nshoppingChannel.Exists():
		print('nshopping list not found')
		exit(1)

	prismWindow.CheckBoxControl(AutomationId="PLSMainView.body.channelsArea.ChannelsArea.TailFrame.GoLivePannel.GoLiveShift").Click()
	nshoppingLiveInfo = prismWindow.WindowControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE")
	thumButton = nshoppingLiveInfo.ImageControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.contentBorder.content.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.thumbnaiBg.thumbnailButton")
	auto.SetCursorPos(x = thumButton.BoundingRectangle.left + int(thumButton.BoundingRectangle.width()*0.5), y =  thumButton.BoundingRectangle.top + int(0.5*thumButton.BoundingRectangle.height()))
	time.sleep(0.4)
	thumButton.ButtonControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.contentBorder.content.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.thumbnaiBg.thumbnailButton.selectButton").Click()

	photoBrower = nshoppingLiveInfo.WindowControl(searchDepth=1)
	address = photoBrower.PaneControl(searchDepth=1, ClassName='WorkerW').PaneControl(ClassName="Address Band Root")
	address.ToolBarControl(ClassName="ToolbarWindow32").Click()
	addEdit = address.EditControl(ClassName='Edit')
	addEdit.GetValuePattern().SetValue(r'C:\Users\Administrator\Pictures\Saved Pictures')
	addEdit.SendKeys('{Enter}')

	photoBrower.PaneControl(AutomationId='main').PaneControl(AutomationId='listview').ListControl(ClassName='UIItemsView').ListItemControl(searchDepth=1, AutomationId='2').DoubleClick()

	nshoppingLiveInfo.WindowControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.PLSCropImage").ButtonControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.PLSCropImage.contentBorder.content.okButton").Click()

	nshoppingLiveInfo.EditControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.contentBorder.content.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.lineEditTitle").GetValuePattern().SetValue('autotest title')
	nshoppingLiveInfo.EditControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.contentBorder.content.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.summaryLineEdit").GetValuePattern().SetValue('autotest summary')

	nshoppingLiveInfo.CheckBoxControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.contentBorder.content.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.shareFirstObject").Click()
	time.sleep(1)
	_menu = _root.WindowControl(searchDepth=1, ClassName='PLSLoadingComboxMenu')
	clickCenterMenuItem(_menu)

	nshoppingLiveInfo.CheckBoxControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.contentBorder.content.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.shareSecondObject").Click()
	time.sleep(1)
	_menu.Refind()
	clickCenterMenuItem(_menu)

	nshoppingLiveInfo.ButtonControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.contentBorder.content.scrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.productWidget.noProductPage.nppAddButton").Click()


	onAirWindow = nshoppingLiveInfo.WindowControl(searchDepth=1, AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.PLSNaverShoppingLIVEProductDialogView")
	onAirWindow.EditControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.PLSNaverShoppingLIVEProductDialogView.contentBorder.content.stackedWidget.storePage.storeSearchBarWidget.storeSearchBar.storeSearchBarLineEdit").GetValuePattern().SetValue('1')

	onAirWindow.ButtonControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.PLSNaverShoppingLIVEProductDialogView.contentBorder.content.stackedWidget.storePage.storeSearchBarWidget.storeSearchBar.storeSearchBarSearchButton").Click()

	time.sleep(2)

	onAirWindow.CustomControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.PLSNaverShoppingLIVEProductDialogView.contentBorder.content.stackedWidget.storePage.storeScrollAreaWidget.storeScrollArea.qt_scrollarea_viewport.storeContent.PLSNaverShoppingLIVEProductItemView").ButtonControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.PLSNaverShoppingLIVEProductDialogView.contentBorder.content.stackedWidget.storePage.storeScrollAreaWidget.storeScrollArea.qt_scrollarea_viewport.storeContent.PLSNaverShoppingLIVEProductItemView.addRemoveButton").Click()

	onAirWindow.ButtonControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.PLSNaverShoppingLIVEProductDialogView.contentBorder.content.bottomWidget.okButton").Click()
	
	nshoppingLiveInfo.ButtonControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveInfoNaverShoppingLIVE.contentBorder.content.bottomFrame.okButton").Click()
	checkNotice(nshoppingLiveInfo)

	time.sleep(5)

	timeLabel = prismWindow.GroupControl(AutomationId="PLSMainView.body.content.PLSBasic.centralwidget.previewContainer.previewTitle").GroupControl(ClassName='PLSTimerDisplay').TextControl(foundIndex=2)

	searchCount = 0
	while True:
		print(timeLabel.Name)
		if '00:00:00' == timeLabel.Name:
			searchCount = searchCount + 1
			time.sleep(5)
			continue

		if searchCount > 5:
			sys.stdout("timeout of live check")
			sys.exit(1)
		break
	prismWindow.CheckBoxControl(AutomationId="PLSMainView.body.channelsArea.ChannelsArea.TailFrame.GoLivePannel.GoLiveShift").Click()

	prismWindow.WindowControl(AutomationId='PLSMainView.body.content.PLSBasic.PLSLiveEndDialog', searchDepth=1).ButtonControl(AutomationId="PLSMainView.body.content.PLSBasic.PLSLiveEndDialog.contentBorder.content.bottomViewWidget.okButton").Click()

	nshoppingChannel.Refind()
	auto.SetCursorPos(x = nshoppingChannel.BoundingRectangle.left + int(nshoppingChannel.BoundingRectangle.width()*0.5), y =  nshoppingChannel.BoundingRectangle.top + int(0.5*nshoppingChannel.BoundingRectangle.height()))
	time.sleep(0.02)
	auto.SetCursorPos(x = nshoppingChannel.BoundingRectangle.left + int(nshoppingChannel.BoundingRectangle.width()*0.5) + 1, y =  nshoppingChannel.BoundingRectangle.top + int(0.5*nshoppingChannel.BoundingRectangle.height()) + 3)
	prismWindow.ButtonControl(AutomationId='PLSMainView.body.channelsArea.ChannelsArea.MidFrame.ChannelScrollArea.qt_scrollarea_viewport.scrollAreaWidgetContents.NormalDisFrame.CapsulesFrame.ChannelCapsule.ChannelConfigPannel.ConfigBtn').Click()

	_root.WindowControl(searchDepth=1, ClassName='QMenu', Name='PRISMLiveStudio').MenuItemControl().Click()
	checkNotice(prismWindow)