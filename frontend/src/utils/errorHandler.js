// src/utils/errorHandler.js

/**
 * Возвращает человекочитаемое сообщение ошибки
 * для alert, toast, banner и т.д.
 */
export function getErrorMessage(error) {
  const data = error?.response?.data

  // Нет ответа от сервера
  if (!data) {
    return 'Network error. Please check your internet connection.'
  }

  // DRF detail
  if (typeof data.detail === 'string') {
    return data.detail
  }

  // DRF non_field_errors
  if (
    Array.isArray(data.non_field_errors) &&
    data.non_field_errors.length
  ) {
    return data.non_field_errors[0]
  }

  // Ошибки полей:
  // email, password, first_name и т.д.
  for (const key in data) {
    const value = data[key]

    if (Array.isArray(value) && value.length) {
      return value[0]
    }

    if (typeof value === 'string') {
      return value
    }
  }

  // На случай если сервер вернул строку
  if (typeof data === 'string') {
    return data
  }

  return 'Something went wrong.'
}

/**
 * Возвращает объект ошибок полей формы.
 *
 * Пример:
 * {
 *   email: ["Already exists"],
 *   password: ["Too short"]
 * }
 */
export function getFieldErrors(error) {
  const data = error?.response?.data

  if (!data || typeof data !== 'object') {
    return {}
  }

  return data
}

/**
 * Проверка, есть ли ошибка у поля
 */
export function hasFieldError(errors, fieldName) {
  return Boolean(errors?.[fieldName]?.length)
}

/**
 * Получить первую ошибку поля
 */
export function getFieldError(errors, fieldName) {
  const fieldErrors = errors?.[fieldName]

  if (
    Array.isArray(fieldErrors) &&
    fieldErrors.length
  ) {
    return fieldErrors[0]
  }

  return ''
}