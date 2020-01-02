
    function addComment(id,commentNum) {

        var that = this;
        var sImageId = id;
        var oCmtIpt = $('#comment'+id);
        var oCommentNum = $('#commentNum'+id);
        var oListDv = $('#js-discuss-list'+id);

        // 点击添加评论
        var bSubmit = false;
        var sCmt = $.trim(oCmtIpt.val());
        // 评论为空不能提交
        if (!sCmt) {
            return alert('评论不能为空');
        }
        // 上一个提交没结束之前，不再提交新的评论
        if (bSubmit) {
            return;
        }
        bSubmit = true;
        $.ajax({
            url: '/comment/add/',
            type: 'post',
            dataType: 'json',
            data: {image_id: sImageId, content: sCmt}
        }).done(function (oResult) {
            if (oResult.code !== 0) {
                return alert(oResult.msg || '提交失败，请重试');
            }
            // 清空输入框
            oCmtIpt.val('');
            // 渲染新的评论
            var sHtml = [
                '<li>',
                    '<a class="_4zhc5 _iqaka" title="', fEncode(oResult.username), '" href="/profile/', oResult.user_id, '">', fEncode(oResult.username), ':</a> ',
                    '<span><span>', fEncode(sCmt), '</span></span>',
                '</li>'].join('');
            oListDv.append(sHtml);
            oCommentNum.html(Number(commentNum)+1)
        }).fail(function (oResult) {
            alert(oResult.msg || '提交失败，请重试');
        }).always(function () {
            bSubmit = false;
        });
    }

    function fEncode(sStr, bDecode) {
        var aReplace =["&#39;", "'", "&quot;", '"', "&nbsp;", " ", "&gt;", ">", "&lt;", "<", "&amp;", "&", "&yen;", "¥"];
        !bDecode && aReplace.reverse();
        for (var i = 0, l = aReplace.length; i < l; i += 2) {
             sStr = sStr.replace(new RegExp(aReplace[i],'g'), aReplace[i+1]);
        }
        return sStr;
    };
