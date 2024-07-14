import request from '@/utils/request.js'

export const getUnhandledReportList = ({ date, page_num, page_size }) => {
    // 获取未处理举报列表
    return request({
        method: 'get',
        url: '/api/manage/commentReports',
        params: {
            mode: 1,
            date,
            page_num,
            page_size
        }
    })
}

export const getHandledReportList = ({ date, page_num, page_size }) => {
    console.log(date, page_num, page_size)
    // 获取已处理举报列表
    return request({
        method: 'get',
        url: '/api/manage/commentReports',
        params: {
            mode: 2,
            date,
            page_num,
            page_size
        }
    })
}

export const getReportDetail = (reportID) => {
    // 获取举报详情
    return request({
        method: 'get',
        url: '/api/manage/commentReportDetail',
        params: {
            report_id: reportID
        }
    })
}

export const judgeReport = ({ report_id, text, visibility }) => {
    // 审核举报
    return request({
        method: 'post',
        url: '/api/manage/judgeCmtRpt',
        data: {
            report_id,
            text,
            visibility
        }
    })
}
