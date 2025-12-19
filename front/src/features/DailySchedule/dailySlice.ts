import { createAsyncThunk, createSlice } from '@reduxjs/toolkit';
import { RootState } from '../../app/store';
import { Iflight } from '../../models/flight';
import { timeout } from '../Profile/profileSlice';
import { getAllFlights, getAllUsers, pullFlights, updateFlight } from './dailyAPI';

export interface dailyState {
  flights: Iflight[]
  refresh: boolean
  users: any[]
}

const initialState: dailyState = {
  flights: [],
  refresh: false,
  users: [],
};

export const getFlightsAsync = createAsyncThunk(
  'daily/getAllFlights',
  async (data:{accessToken: string,date:string}) => {
    const response = await getAllFlights(data.accessToken,data.date);
    return response;
  }
);
export const pullFlightsAsync = createAsyncThunk(
  'daily/pullFlights',
  async () => {
    const response = await pullFlights();
    return response;
  }
);
export const getAllUsersAsync = createAsyncThunk(
  'daily/getAllUsers',
  async () => {
    const response = await getAllUsers();
    return response;
  }
);
export const updateFlightAsync = createAsyncThunk(
  'daily/updateFlight',
  async (obj: { flight: any, accessToken: string }) => {
    const response = await updateFlight(obj);
    return response;
  }
);

export const dailySlice = createSlice(
  {
    name: 'daily',
    initialState,
    reducers: {
    },
    extraReducers: (builder) => {
      builder
        .addCase(getFlightsAsync.fulfilled, (state, action) => {
          state.flights = action.payload.sort((a:Iflight, b:Iflight) => +new Date(a.stdLocal) - +new Date(b.stdLocal))
        })
        .addCase(getFlightsAsync.rejected, (state) => {
          timeout()
        })
        .addCase(pullFlightsAsync.fulfilled, (state) => {
          state.refresh = !state.refresh
        })
        .addCase(getAllUsersAsync.fulfilled, (state, action) => {
          state.users = action.payload
        })
        .addCase(getAllUsersAsync.rejected, (state) => {
          timeout()
        })
        .addCase(updateFlightAsync.fulfilled, (state) => {
          state.refresh = !state.refresh
        })
    },
  });

// export const { } = dailySlice.actions;

export const selectFlights = (state: RootState) => state.daily.flights;
export const selectFlightsRefresh = (state: RootState) => state.daily.refresh;
export const selectAllUsers = (state: RootState) => state.daily.users;

export default dailySlice.reducer;