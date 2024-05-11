// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-nocheck
import { action, atom, batch, createCtx } from '@reatom/core'

export const ctx = createCtx()

export const countryAtom = atom('Uzb')
export const pageAtom = atom(1)

// atom to store table data
export const dataAtom = atom(new Array())
export const fetchErrorAtom = atom(null)


// atom to know total number of pages of data
export const totalPagesAtom = atom(1)
// atom to store pagination
export const paginationAtom = atom(new Array())

// atom for table columns
export const columnsAtom = atom(new Array())

const ApiUrl = 'http://localhost:8000/'

// atom for api url
export const apiUrlAtom = atom((ctx) => {
  const page = ctx.spy(pageAtom)
  const country = ctx.spy(countryAtom)

  let urlAtom = `${ApiUrl}`

  if (country === '') {
    urlAtom = `${ApiUrl}uzb`
  }
  if (country !== '') {
    urlAtom = `${urlAtom}${country.toLowerCase()}`
  }
  if (page !== 0) {
    urlAtom = `${urlAtom}?page=${page}`
  }
  return urlAtom
})

export const fetchData = action(async (ctx) => {
  const url = ctx.get(apiUrlAtom)

  const data = await ctx.schedule( async() => {
    const response = await fetch(url)

    if (!response.ok) {
      let errorMsg
      if (response.status === 404) {
        errorMsg = 'Data Not Found'
      }
      batch(ctx, () => {
        fetchErrorAtom(ctx, errorMsg)
        dataAtom(ctx, new Array())
        pageAtom(ctx, 1)
        totalPagesAtom(ctx, 1)
        paginationAtom(ctx, new Array())
        columnsAtom(ctx, new Array())
      })

    } else {
      fetchErrorAtom(ctx, null)
    }

    const json = await response.json()
    return json
  })

  if (ctx.get(fetchErrorAtom)) {
    return
  }

  batch(ctx, () => {
    dataAtom(ctx, data.data)
    totalPagesAtom(ctx, data.pages)
    columnsAtom(ctx, data.columns)

    const totalPages = data.pages
    const page = data.page
    if (totalPages <= 5) {
      paginationAtom(ctx, [1, 2, 3, 4, 5].splice(0, data.total))
    } else {
      let pages
      if (page <=3 ) {
        pages = [1, 2, 3, 4, '...', totalPages]
      }
      if (page > 3 && page < totalPages - 2) {
        pages = [1, '...', page - 1,  page, page + 1, '...', totalPages]
      }
      if (page >= totalPages - 2) {
        pages = [1, '...', totalPages - 3, totalPages - 2, totalPages - 1, totalPages]
      }
      paginationAtom(ctx, pages)
    }
  })
})

pageAtom.onChange(fetchData)
countryAtom.onChange(fetchData)
