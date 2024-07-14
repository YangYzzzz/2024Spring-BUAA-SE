import enquireJs from 'enquire.js'

export function isDef (v){
  return v !== undefined && v !== null
}

/**
 * Remove an item from an array.
 */
export function remove (arr, item) {
  if (arr.length) {
    const index = arr.indexOf(item)
    if (index > -1) {
      return arr.splice(index, 1)
    }
  }
}

export function isRegExp (v) {
  return _toString.call(v) === '[object RegExp]'
}

export function enquireScreen(call) {
  const handler = {
    match: function () {
      call && call(true)
    },
    unmatch: function () {
      call && call(false)
    }
  }
  enquireJs.register('only screen and (max-width: 767.99px)', handler)
}

const _toString = Object.prototype.toString

export const getErrModalOptions = err => {
  const title = 'Error ' + (err.status || '')
  const errData = err.response ? err.response.data || err : err
  // to see a rendered django debug info page
  // do not cast string-type errData
  const content = typeof errData === 'string' ? errData : JSON.stringify(errData, null, 2)
  return {
    title,
    content
  }
}

export const getLocalTime = (utcTime) => {
  if (utcTime === null || utcTime === undefined) {
    return '无'
  } else {
    let date = new Date(utcTime)
    const second = date.getSeconds() < 10 ? '0' + date.getSeconds() : date.getSeconds()
    const min = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes()
    const hour = date.getHours() < 10 ? '0' + date.getHours() : date.getHours()
    // if (isHour) {
    //   return `${hour}:${min}:${second}`
    // }
    return `${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()} ${hour}:${min}:${second}`
  }
}
