#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
FX 資金管理アプリ
・FXのトレードにおける最適Lot数を求めるアプリ
最適Lot数 = (リスク許容額 / リスク許容幅)  * 円換算率
リスク許容額 = 資金　*　損切率（％）
リスク許容幅 = 見込み利確幅　/ 利益率
"""
import wx
import math
# begin wxGlade: dependencies
# end wxGlade

# begin wxGlade: extracode
# end wxGlade


class MyFrame(wx.Frame):
    # コンストラクタ
    def __init__(self, *args, **kwds):
        # ウィンドウ設定
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((640, 480))
        self.SetTitle(u"資金管理アプリ")

        # パネルセット
        self.main_panel = wx.Panel(self, wx.ID_ANY)
        self.main_panel.SetMinSize((640, 480))
        self.sizer_input_output = wx.BoxSizer(wx.VERTICAL)
        # -----------

        # 入力インターフェース
        self.meigara_box = wx.ComboBox(self.main_panel, wx.ID_ANY,
                                       choices=["USD/JPY", "GBP/JPY", "EUR/JPY", "AUD/JPY",
                                                "GBP/USD", "EUR/USD", "AUD/USD",
                                                "JP255", "US30", "GOLD"], style=wx.CB_DROPDOWN)
        self.input_rikakuhaba = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, initial=0.0, min=0.0, max=1000.0,
                                                  style=0)
        self.input_profitrate = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, initial=3.0, min=0.0, max=100.0)
        self.input_enkanzan = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, initial=100, min=0, max=400, style=0)
        self.input_songiri = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, initial=2.0, min=0.0, max=10.0)
        self.input_syokokin = wx.SpinCtrlDouble(self.main_panel, wx.ID_ANY, initial=100000.0, min=0.0, max=10000000.0)
        self.space_4 = wx.Panel(self.main_panel, wx.ID_ANY)

        # 出力結果表示テキスト
        self.output_risukukyoyougaku = wx.StaticText(self.main_panel, wx.ID_ANY, "-")
        self.output_sonekihiritu = wx.StaticText(self.main_panel, wx.ID_ANY, "1 : x")
        self.output_kyoyouhaba = wx.StaticText(self.main_panel, wx.ID_ANY, "-")
        self.output_saitekilot = wx.StaticText(self.main_panel, wx.ID_ANY, "-")

        # 計算用変数
        self.enkanzan_rate = 0.001
        # -----------

        # 入力エリアセット
        self.sizer_input = wx.GridSizer(2, 8, 5, 5)
        self.sizer_input_output.Add(self.sizer_input, 1, wx.ALL | wx.EXPAND, 0)
        self.initInput()
        input_line = wx.StaticLine(self.main_panel, wx.ID_ANY)
        self.sizer_input_output.Add(input_line, 0, wx.EXPAND, 0)
        # -----------

        # 出力エリアセット
        self.sizer_output = wx.FlexGridSizer(2, 6, 5, 5)
        self.sizer_input_output.Add(self.sizer_output, 1, wx.ALL | wx.EXPAND, 0)
        self.initOutput()
        output_line = wx.StaticLine(self.main_panel, wx.ID_ANY)
        self.sizer_input_output.Add(output_line, 0, wx.EXPAND, 0)
        # -----------

        # メインパネルにセット
        self.main_panel.SetSizer(self.sizer_input_output)
        self.Layout()

        # イベント処理
        self.main_panel.Bind(wx.EVT_LEFT_DOWN, self.OnMouceLeft)
        self.meigara_box.Bind(wx.EVT_COMBOBOX, self.MeigaraSentaku)
        # end wxGlade

    # -------------------------------------------------------------------------------------------------------------

    # 画面上でマウスをクリックすると計算処理を行う
    def OnMouceLeft(self, event):
        obj = event.GetEventObject().GetParent()
        obj.SetFocus()
        self.calcBestLot()

    # レイアウトの初期化
    def resetLayout(self):
        self.output_saitekilot.SetLabel("-")
        self.output_kyoyouhaba.SetLabel(str(0.00))
        self.output_sonekihiritu.SetLabel("1 : -")
        self.output_risukukyoyougaku.SetLabel("-")
        self.sizer_input_output.Layout()

    # 最適Lot計算処理
    def calcBestLot(self):
        self.resetLayout()
        self.MeigaraSentaku(event=None)

        # リスク許容額 = 資金　*　損切りルール(%)
        _kyoyougaku = self.input_syokokin.GetValue() * self.input_songiri.GetValue() * 0.01

        # リスク許容幅 = 見込み利確幅　/ 利益率
        _risukuhaba = self.input_rikakuhaba.GetValue() / self.input_profitrate.GetValue()

        # 最適Lot
        if _kyoyougaku != 0 and _risukuhaba != 0:
            _lot = (_kyoyougaku / _risukuhaba) * self.enkanzan_rate

            # 出力
            self.output_risukukyoyougaku.SetLabel(str(round(_kyoyougaku, 0)))
            self.output_kyoyouhaba.SetLabel(str(round(_risukuhaba, 2)))
            self.output_sonekihiritu.SetLabel("1 : " + str(round(self.input_profitrate.GetValue(), 2)))
            self.output_saitekilot.SetLabel(str(round(_lot, 2)))

        # レイアウト調整
        self.sizer_input_output.Layout()

    # 銘柄が日本円ペア、クロス円、CFD、コモンズで円換算率が異なる
    def MeigaraSentaku(self, event):
        _select = self.meigara_box.GetSelection()
        if _select < 4 or _select == 7:
            # 最小取引数量 = 0.01Lot
            self.enkanzan_rate = 1 * 0.01
        else:
            # # 最小取引数量 = 0.0001ドル
            self.enkanzan_rate = (1 / self.input_enkanzan.GetValue())

        if event is not None:
            self.calcBestLot()

    # 入力インタフェースの細かい設定
    def initInput(self):
        text_input_syokokin = wx.StaticText(self.main_panel, wx.ID_ANY, u"有効証拠金 :")
        self.sizer_input.Add(text_input_syokokin, 0, wx.ALIGN_CENTER | wx.LEFT | wx.SHAPED, 5)

        self.input_syokokin.SetIncrement(1.0)
        self.input_syokokin.SetDigits(1)
        self.sizer_input.Add(self.input_syokokin, 0, wx.ALIGN_CENTER | wx.LEFT, 25)

        text_syokokin_tani = wx.StaticText(self.main_panel, wx.ID_ANY, u"円")
        self.sizer_input.Add(text_syokokin_tani, 0, wx.ALIGN_CENTER | wx.RIGHT, 5)

        text_input_songiri = wx.StaticText(self.main_panel, wx.ID_ANY, u"損切ルール :")
        self.sizer_input.Add(text_input_songiri, 0, wx.ALIGN_CENTER | wx.RIGHT, 50)

        self.input_songiri.SetIncrement(0.1)
        self.input_songiri.SetDigits(1)
        self.sizer_input.Add(self.input_songiri, 0, wx.ALIGN_CENTER | wx.RIGHT, 50)

        text_songiri_tani = wx.StaticText(self.main_panel, wx.ID_ANY, "%")
        self.sizer_input.Add(text_songiri_tani, 0, wx.ALIGN_CENTER | wx.RIGHT, 110)

        text_input_usd = wx.StaticText(self.main_panel, wx.ID_ANY, u"円換算 :")
        self.sizer_input.Add(text_input_usd, 0, wx.ALIGN_CENTER | wx.RIGHT, 180)

        self.input_enkanzan.SetIncrement(1)
        self.input_enkanzan.SetDigits(0)
        self.sizer_input.Add(self.input_enkanzan, 0, wx.ALIGN_CENTER | wx.RIGHT, 200)

        text_input_syoritu = wx.StaticText(self.main_panel, wx.ID_ANY, u"利確率 :")
        self.sizer_input.Add(text_input_syoritu, 0, wx.ALIGN_CENTER | wx.LEFT, 5)

        self.input_profitrate.SetIncrement(0.1)
        self.input_profitrate.SetDigits(1)
        self.sizer_input.Add(self.input_profitrate, 0, wx.ALIGN_CENTER, 0)

        text_syoritu_tani = wx.StaticText(self.main_panel, wx.ID_ANY, "倍")
        self.sizer_input.Add(text_syoritu_tani, 0, wx.ALIGN_CENTER | wx.RIGHT, 60)

        text_input_rikakuhaba = wx.StaticText(self.main_panel, wx.ID_ANY, u"見込み利確幅 :")
        self.sizer_input.Add(text_input_rikakuhaba, 0, wx.ALIGN_CENTER | wx.RIGHT, 90)

        self.input_rikakuhaba.SetDigits(0)
        self.sizer_input.Add(self.input_rikakuhaba, 0, wx.ALIGN_CENTER | wx.RIGHT, 85)

        text_rikakuhaba_tani = wx.StaticText(self.main_panel, wx.ID_ANY, "ポイント")
        self.sizer_input.Add(text_rikakuhaba_tani, 0, wx.ALIGN_CENTER | wx.RIGHT, 135)

        text_meigara = wx.StaticText(self.main_panel, wx.ID_ANY, u"銘柄 :")
        self.sizer_input.Add(text_meigara, 0, wx.ALIGN_CENTER | wx.RIGHT, 185)

        self.meigara_box.SetSelection(0)
        self.sizer_input.Add(self.meigara_box, 0, wx.ALIGN_CENTER | wx.RIGHT, 220)

    # 出力インタフェースの細かい設定
    def initOutput(self):
        text_output_kyoyougaku = wx.StaticText(self.main_panel, wx.ID_ANY, u"リスク許容額 :")
        self.sizer_output.Add(text_output_kyoyougaku, 0, wx.ALIGN_CENTER | wx.LEFT, 15)

        self.output_risukukyoyougaku.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.sizer_output.Add(self.output_risukukyoyougaku, 0, wx.ALIGN_CENTER | wx.ALL, 0)

        text_kyoyougaku_tani = wx.StaticText(self.main_panel, wx.ID_ANY, u"円")
        self.sizer_output.Add(text_kyoyougaku_tani, 0, wx.ALIGN_CENTER, 0)

        text_input_sonekihiritu = wx.StaticText(self.main_panel, wx.ID_ANY, u"損益比率 :")
        self.sizer_output.Add(text_input_sonekihiritu, 0, wx.ALIGN_CENTER | wx.LEFT, 11)

        self.output_sonekihiritu.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.sizer_output.Add(self.output_sonekihiritu, 0, wx.ALIGN_CENTER, 0)

        self.sizer_output.Add(self.space_4, 1, wx.ALL | wx.EXPAND, 0)

        text_kyoyouhaba = wx.StaticText(self.main_panel, wx.ID_ANY, u"リスク許容幅 :")
        self.sizer_output.Add(text_kyoyouhaba, 0, wx.ALIGN_CENTER | wx.LEFT, 15)

        self.output_kyoyouhaba.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.sizer_output.Add(self.output_kyoyouhaba, 0, wx.ALIGN_CENTER, 0)

        text_kyoyouhaba_tani = wx.StaticText(self.main_panel, wx.ID_ANY, "ポイント")
        self.sizer_output.Add(text_kyoyouhaba_tani, 0, wx.ALIGN_CENTER, 0)

        text_saitekilot = wx.StaticText(self.main_panel, wx.ID_ANY, u"最適Lot数 :")
        self.sizer_output.Add(text_saitekilot, 0, wx.ALIGN_CENTER | wx.LEFT, 15)

        self.output_saitekilot.SetFont(
            wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, 0, ""))
        self.sizer_output.Add(self.output_saitekilot, 0, wx.ALIGN_CENTER, 0)

        text_saitekilot_tani = wx.StaticText(self.main_panel, wx.ID_ANY, "Lot")
        self.sizer_output.Add(text_saitekilot_tani, 0, wx.ALIGN_CENTER, 0)


# end of class MyFrame

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True


# end of class MyApp

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()
